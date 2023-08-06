import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pyttsx3


class StockAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.download_data()

    def download_data(self):
        valid_tickers = []
        for ticker in self.tickers:
            try:
                data = yf.download(ticker, period="1d")
                if not data.empty:
                    valid_tickers.append(ticker)
                else:
                    print(f"{ticker}: No data found, symbol may be delisted")
            except Exception as e:
                print(f"Failed to download {ticker}: {e}")
        self.tickers = valid_tickers
        us_price_data = yf.download(self.tickers, period="1d").dropna(axis=1)
        self.price, self.volume = us_price_data["Adj Close"], us_price_data["Volume"]

    def plot(self):
        plt.style.use("dark_background")
        plt.figure(figsize=(15, 6))
        n_tickers = len(self.tickers)
        colors = plt.cm.rainbow(np.linspace(0, 1, n_tickers))
        fig, axs = plt.subplots(3, 1, figsize=(15, 22))

        axs[0].scatter(
            self.volume.iloc[0, :n_tickers], self.price.iloc[0, :n_tickers], c=colors
        )
        axs[1].bar(self.price.columns[:n_tickers], self.price.iloc[0, :n_tickers])
        axs[2].bar(self.volume.columns[:n_tickers], self.volume.iloc[0, :n_tickers])

        for i, (vol, prc, symbol) in enumerate(
            zip(
                self.volume.iloc[0, :n_tickers],
                self.price.iloc[0, :n_tickers],
                self.volume.columns[:n_tickers],
            )
        ):
            axs[0].annotate(symbol, (vol, prc), color=colors[i])
            axs[1].get_xticklabels()[i].set_text(symbol)
            axs[2].get_xticklabels()[i].set_text(symbol)

        # Add grid to each subplot
        for ax in axs:
            ax.grid(color="white", linestyle="--", linewidth=1, alpha=0.5)

        # Use EngFormatter for the y-axis of the Volume plot
        axs[2].yaxis.set_major_formatter(ticker.EngFormatter())

        axs[0].set_title("Stocks: Volume vs. Price")
        axs[0].set_xlabel("Volume")
        axs[0].set_ylabel("Price")
        axs[1].set_title("Stocks: Price")
        axs[1].set_xlabel("Symbol")
        axs[1].set_ylabel("Price")
        axs[2].set_title("Stocks: Volume")
        axs[2].set_xlabel("Symbol")
        axs[2].set_ylabel("Volume")
        plt.show()

    def speak(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)
        text = "Stocks: " + ", ".join(
            f"{symbol} with a price of {round(prc,2)}"
            for symbol, prc in zip(
                self.volume.columns[: len(self.tickers)],
                self.price.iloc[0, : len(self.tickers)],
            )
        )
        engine.say(text)
        engine.runAndWait()
        engine.save_to_file(text, "output.mp3")
        engine.runAndWait()


# # Example usage:
# tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
# stock_analyzer = StockAnalyzer(tickers)
# stock_analyzer.plot()
# stock_analyzer.speak()
