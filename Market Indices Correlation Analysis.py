import yfinance as yf
import pandas as pd


# Calculate daily returns for each ticker
def calculate_daily_returns(data):
    return data['Adj Close'].pct_change().dropna()


# Calculate correlation between indices and respective tickers
def compute_correlation_with_index(stock_returns, index_returns):
    correlation = stock_returns.corrwith(index_returns)
    return correlation


# Tickers for DJIA and Nasdaq_100
djia_tickers = ["AAPL", "MSFT", "AMZN", "JPM", "WMT", "V", "UNH", "PG", "JNJ", "HD",
                "MRK", "CVX", "KO", "CRM", "CSCO", "MCD", "DIS", "VZ", "AXP", "AMGN",
                "IBM", "CAT", "GS", "INTC", "HON", "BA", "NKE", "MMM", "TRV", "DOW"]

nasdaq_tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "AVGO", "ASML",
                  "COST", "NFLX", "AMD", "ADBE", "AZN", "QCOM", "PEP", "TMUS", "AMAT", "LIN",
                  "CSCO", "PDD", "TXN", "INTU", "AMGN", "ISRG", "INTC", "CMCSA", "LRCX", "MU",
                  "HON", "BKNG", "VRTX", "KLAC", "ADI", "REGN", "PANW", "ABNB", "ADP", "CRWD",
                  "SNPS", "MDLZ", "MELI", "CDNS", "GILD", "SBUX", "CTAS", "NXPI", "CEG", "MAR",
                  "MRVL", "CSX", "PYPL", "ORLY", "WDAY", "ROP", "PCAR", "ADSK", "CPRT", "MNST",
                  "TTD", "MCHP", "ROST", "TEAM", "AEP", "FTNT", "DASH", "MRNA", "DXCM", "KDP",
                  "DDOG", "CHTR", "PAYX", "IDXX", "VRSK", "KHC", "ODFL", "EA", "FANG", "FAST",
                  "GEHC", "LULU", "EXC", "BKR", "BIIB", "CTSH", "CCEP", "ON", "ZS", "GFS",
                  "CSGP", "XEL", "CDW", "ANSS", "TTWO", "DLTR", "MDB", "WBD", "ILMN", "SIRI",
                  "WBA"]

# Range of data retrieval
start_date = "2021-07-08"
end_date = "2024-07-07"

# Download data for DJIA and Nasdaq_100 tickers
djia_data = yf.download(tickers=djia_tickers, start=start_date, end=end_date)
nasdaq_data = yf.download(tickers=nasdaq_tickers, start=start_date, end=end_date)

# Calculate daily returns for each ticker
djia_returns = calculate_daily_returns(djia_data)
nasdaq_returns = calculate_daily_returns(nasdaq_data)

# Download data for DJIA and Nasdaq_100 indices
djia_index = yf.download("^DJI", start=start_date, end=end_date)
nasdaq_index = yf.download("^NDX", start=start_date, end=end_date)

# Calculate daily returns for each indice
djia_index_returns = djia_index["Adj Close"].pct_change().dropna()
nasdaq_index_returns = nasdaq_index["Adj Close"].pct_change().dropna()

# Calculate correlation between indices and respective tickers
djia_correlations = compute_correlation_with_index(djia_returns, djia_index_returns)
nasdaq_correlations = compute_correlation_with_index(nasdaq_returns, nasdaq_index_returns)

# Identify stocks with high correlation with their indices
high_corr_djia = djia_correlations[djia_correlations > 0.7]
high_corr_nasdaq = nasdaq_correlations[nasdaq_correlations > 0.7]

# Print stocks with high correlation with their indices
print("DJIA stocks with high correlation (>0.7) with the DJIA index:")
print(high_corr_djia)

print("\nNasdaq stocks with high correlation (>0.7) with the Nasdaq index:")
print(high_corr_nasdaq)
