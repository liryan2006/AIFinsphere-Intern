import tushare as ts
import pandas as pd
import time
from statsmodels.tsa.stattools import adfuller

# Setup Tushare API
ts.set_token('756a1f4aba6dd90ced168a81497f46697c8499ccfa76b317daf6e874')
pro = ts.pro_api()

# Fetch all ETF tickers
etf_info = pro.fund_basic(market='E')
tickers = etf_info['ts_code'].tolist()

# Define analysis period
start_date = '20240101'
end_date = '20240601'

# Collect tickers which data can be retrieved
retrieved_tickers = []


# Fetch data in batches to avoid API retrieval rate limit
def fetch_data_in_batches(batch_size=250, delay=40):
    etf_data_dict = {}
    total_tickers = len(tickers)
    for i in range(0, total_tickers, batch_size):
        batch_tickers = tickers[i:i + batch_size]
        for ticker in batch_tickers:
            df = pro.fund_daily(ts_code=ticker, start_date=start_date, end_date=end_date)
            if len(df) > 5:  # Ignore tickers with little data (less than 5 days)
                retrieved_tickers.append(ticker)
                etf_data_dict[ticker] = df[['trade_date', 'open', 'close']]
        print(f"Fetched batch {i // batch_size + 1}/{(total_tickers // batch_size) + 1}")
        time.sleep(delay)   # Wait 40 seconds
    return etf_data_dict


# Filter datas through autocorrelation
def autocorrelation_filter(threshold):
    high_autocorr = {'Ticker': [], 'Autocorrelation': [], 'Start Time': [], 'End Time': []}
    for ticker in retrieved_tickers:
        data = etf_dict[ticker]
        autocorr = data['close'].autocorr()
        if autocorr >= threshold:
            # Find start & end date for each ETF, which are potentially different from start_date or
            # end_date due to missing data
            start_time = data['trade_date'][len(data) - 1]
            end_time = data['trade_date'][0]

            # Add ETF properties to Dataframe
            high_autocorr['Ticker'].append(ticker)
            high_autocorr['Autocorrelation'].append(autocorr)
            high_autocorr['Start Time'].append(start_time)
            high_autocorr['End Time'].append(end_time)
    return pd.DataFrame(high_autocorr)


# Filter datas through stationarity
def stationarity_filter(threshold):
    low_stationarity = {'Ticker': [], 'Start Time': [], 'End Time': []}
    for ticker in retrieved_tickers:
        data = etf_dict[ticker]
        adf_result = adfuller(data['close'])
        p_value = adf_result[1]
        if p_value > threshold:
            # Find start & end date for each ETF
            start_time = data['trade_date'][len(data) - 1]
            end_time = data['trade_date'][0]

            # Add ETF properties to Dataframe
            low_stationarity['Ticker'].append(ticker)
            low_stationarity['Start Time'].append(start_time)
            low_stationarity['End Time'].append(end_time)
    return pd.DataFrame(low_stationarity)


# Find intersection between previously filtered datas
def intersection_filter(autocorr_df, stationarity_df):
    # Get sets of tickers from both DataFrames
    autocorr_tickers = set(autocorr_df['Ticker'])
    stationarity_tickers = set(stationarity_df['Ticker'])

    # Find the intersection of the two sets
    common_tickers = autocorr_tickers & stationarity_tickers
    return common_tickers


etf_dict = fetch_data_in_batches()

autocorr_threshold = 0.95   # Set autocorrelation threshold
autocorr_etfs = autocorrelation_filter(autocorr_threshold)

significance_level = 0.6    # Set significance level for stationarity
stationarity_etfs = stationarity_filter(significance_level)

shared_tickers = intersection_filter(autocorr_etfs, stationarity_etfs)

print("Selected ETFs based on autocorrelation:")
print(autocorr_etfs)
print("Selected ETFs based on stationarity:")
print(stationarity_etfs)
print("Commonly selected ETFs:")
print(shared_tickers)
