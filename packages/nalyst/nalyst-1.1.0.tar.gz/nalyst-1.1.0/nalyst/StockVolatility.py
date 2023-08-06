import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyttsx3
import seaborn as sns
import yfinance as yf
import datetime


class TextToSpeech:
    def __init__(self, text, rate=140, volume=1.0):
        self.text = text
        self.rate = rate
        self.volume = volume
        self.engine = pyttsx3.init()

    def speak(self):
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self.engine.say(self.text)
        self.engine.runAndWait()
        self.engine.stop()

    def save_to_file(self, file_name):
        self.engine.save_to_file(self.text, file_name)
        self.engine.runAndWait()


def stock_volatility(close_prices):

    daily_returns = close_prices.pct_change().dropna()
    standard_deviation = np.std(daily_returns)

    if standard_deviation < 0.05:
        result = f"The standard deviation of the stock's daily returns is {standard_deviation:.4f}. This stock can be considered relatively safe to trade."
    elif standard_deviation >= 0.05 and standard_deviation < 0.1:
        result = f"The standard deviation of the stock's daily returns is {standard_deviation:.4f}. This stock is moderately safe to trade."
    else:
        result = f"The standard deviation of the stock's daily returns is {standard_deviation:.4f}. This stock is considered risky to trade."

    # Plot the daily returns
    plt.style.use('dark_background')
    plt.figure(figsize=(15, 6))
    plt.plot(daily_returns, label="Stock Daily Returns")
    # Plot the standard deviation
    plt.axhline(standard_deviation, color='red',
                label=f"Standard Deviation ({standard_deviation:.4f})")
    plt.grid(color='white', linestyle='--', linewidth=1, alpha=0.5)
    # Add title, labels, and legend
    plt.title("Stock Daily Returns and Standard Deviation")
    plt.xlabel("Time")
    plt.ylabel("Returns")
    plt.legend()
    # Show the plot
    plt.show()

    print(result)
    tts = pyttsx3.init()
    tts.setProperty('rate', 160)
    tts.say(result)
    tts.runAndWait()


# stock = yf.Ticker(str(str(input(" Enter your stock ticker: ").upper())))
# stock = stock.history(period=input(" Enter Number of days (eg 365d): "))
# stock = stock.Close
# stock_volatility(stock)
