import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


class MonteCarloSimulator:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.data = yf.download(symbol, start=start_date, end=end_date)[
            'Adj Close']
        self.returns = np.log(1 + self.data.pct_change())
        self.mu = self.returns.mean()
        self.sigma = self.returns.std()

    def generate_paths(self, num_paths, num_days):
        T = num_days
        N = num_paths
        S0 = self.data.iloc[-1]
        dt = 1 / T

        paths = np.zeros((T, N))
        paths[0] = S0
        for t in range(1, T):
            drift = (self.mu - 0.5 * self.sigma ** 2) * dt
            diffusion = self.sigma * np.sqrt(dt) * np.random.normal(size=N)
            paths[t] = paths[t-1] * np.exp(drift + diffusion)

        return paths

    def plot_paths(self, num_paths, num_days):
        paths = self.generate_paths(num_paths, num_days)
        plt.style.use('dark_background')
        plt.figure(figsize=(15, 6))
        plt.plot(paths)
        plt.xlabel('Trading Days')
        plt.ylabel('Stock Price')
        plt.title('Monte Carlo Simulation for ' + self.symbol)
        plt.grid(linestyle='--', color='gray', alpha=0.5)
        plt.show()
