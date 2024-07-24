from finvizfinance.screener.overview import Overview
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


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


print(get_etf_tickers())
