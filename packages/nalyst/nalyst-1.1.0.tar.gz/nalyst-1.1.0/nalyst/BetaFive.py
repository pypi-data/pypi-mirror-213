import yfinance as yf
import numpy as np


def calculate_beta_five(ticker, benchmark):
    try:
        stock = yf.Ticker(ticker).history(period="5y", interval='1mo')
        benchmark = yf.Ticker(benchmark).history(period="5y", interval='1mo')

        # Align the dates of stock and benchmark DataFrames
        stock, benchmark = stock.align(benchmark, join='inner', axis=0)

        stock_returns = stock['Close'].pct_change().dropna()
        benchmark_returns = benchmark['Close'].pct_change().dropna()

        covariance = np.cov(stock_returns, benchmark_returns)[0][1]
        benchmark_variance = np.var(benchmark_returns)

        beta = covariance / benchmark_variance
        return beta
    except Exception as e:
        print(f"Error: Invalid ticker symbol - {e}")
        return None
