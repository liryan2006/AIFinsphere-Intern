from finvizfinance.screener.overview import Overview
import warnings
import yfinance as yf

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_etf_tickers():
    # Initialize the Overview object
    screener = Overview()

    # Configure the screener for ETFs using filters_dict
    filters_dict = {'Industry': 'Exchange Traded Fund'}  # Filter for ETFs
    screener.set_filter(filters_dict=filters_dict)

    # Retrieve the tickers
    etf_df = screener.screener_view(order='Ticker', limit=3, verbose=1, ascend=True)
    tickers = etf_df['Ticker'].tolist()

    return tickers


def download_etf_data(tickers):
    # Set fixed end date
    end_date = '2024-06-20'
    start_date = '2023-06-21'

    for ticker in tickers:
        try:
            # Download data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date)

            # Check if data is not empty
            if not data.empty:
                # Save to CSV
                data.to_csv(f'{ticker}.csv')
                print(f'Successfully downloaded data for {ticker}')
            else:
                print(f'No data found for {ticker}')
        except Exception as e:
            print(f'Error downloading data for {ticker}: {e}')


etf_tickers = get_etf_tickers()
download_etf_data(etf_tickers)

