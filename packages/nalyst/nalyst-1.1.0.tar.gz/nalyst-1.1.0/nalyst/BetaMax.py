import yfinance as yf
import numpy as np


def calculate_beta_max(ticker, benchmark_ticker):
    try:
        # Fetch historical price data for the stock and benchmark
        stock = yf.Ticker(ticker).history(period="max")
        benchmark = yf.Ticker(benchmark_ticker).history(period="max")
    except ValueError:
        # Catch ValueError exception if ticker symbol is invalid
        return "Invalid ticker symbol"

    # Calculate daily percentage change in closing prices for the stock and benchmark
    stock_returns = stock['Close'].pct_change().dropna()
    benchmark_returns = benchmark['Close'].pct_change().dropna()

    # Truncate returns to the same length
    min_len = min(len(stock_returns), len(benchmark_returns))
    stock_returns = stock_returns[-min_len:]
    benchmark_returns = benchmark_returns[-min_len:]

    # Calculate covariance and benchmark variance
    covariance = np.cov(stock_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)

    # Calculate beta
    beta = covariance / benchmark_variance

    return beta
