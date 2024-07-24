import warnings
import yfinance as yf
import time
from finvizfinance.screener.overview import Overview

# Suppress unnecessary warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Obtain a real-time list of ETF tickers via Finviz API
def get_etf_tickers():
    # Initialize the Overview object
    screener = Overview()

    # Configure the screener for ETFs using filters_dict
    filters_dict = {'Industry': 'Exchange Traded Fund'}  # Filter for ETFs
    screener.set_filter(filters_dict=filters_dict)

    # Retrieve the tickers
    etf_df = screener.screener_view(order='Ticker', verbose=1, ascend=True)
    tickers = etf_df['Ticker'].tolist()

    return tickers


# Download ETF historical price data using Yahoo Finance API
def download_etf_data(tickers, batch_size=2000, sleep_time=3600):
    # Set start and end date
    end_date = '2024-06-20'
    start_date = '2023-06-21'

    # Download data in batches to respect yFinance API rate limit of 2000 requests per hour
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1}: {batch}")

        for ticker in batch:
            try:
                # Download data from Yahoo Finance
                data = yf.download(ticker, start=start_date, end=end_date)

                # Check if data is not empty
                if not data.empty:
                    # Save data to CSV
                    data.to_csv(f'{ticker}.csv')
                    print(f'Successfully downloaded data for {ticker}')
                else:
                    print(f'No data found for {ticker}')
            except Exception as e:
                print(f'Error downloading data for {ticker}: {e}')

        # Sleep between batches
        if i + batch_size < len(tickers):
            print(f"Sleeping for {sleep_time / 60} minutes between batches...")
            time.sleep(sleep_time)


if __name__ == '__main__':
    # Retrieve ETF Tickers
    etf_tickers = get_etf_tickers()

    # Download and save ETF data to CSV Files
    download_etf_data(etf_tickers)

