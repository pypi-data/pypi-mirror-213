import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyttsx3
import seaborn as sns
import yfinance as yf
import datetime

# stock price


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

    def price(self):
        return yf.download(self.ticker)

# LinearModel


class LinearModel:
    def LinearRegression(self, x, y):
        n = len(x)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)
        sum_x2 = np.sum(x ** 2)
        b1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        bo = (sum_y - b1 * sum_x) / n
        return b1, bo

# Plotting graph


class Plot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def ScatterPlot(self, x_pred, y_pred):
        plt.style.use('dark_background')
        plt.figure(figsize=(15, 6))
        residuals = self.y - y_pred
        above_line = self.x[np.where(residuals >= 0)]
        below_line = self.x[np.where(residuals < 0)]
        y_above_line = self.y[np.where(residuals >= 0)]
        y_below_line = self.y[np.where(residuals < 0)]
        sns.scatterplot(x=above_line, y=y_above_line, color="red",
                        alpha=0.5, label="Above best-fit line")
        sns.scatterplot(x=below_line, y=y_below_line,
                        color="white", alpha=0.5, label="Below best-fit line")
        sns.lineplot(x=self.x, y=y_pred, color="yellow", label="Best-fit line")
        plt.xlabel("Stock A")
        plt.ylabel("Stock B")
        plt.grid(color='white', linestyle='--', linewidth=1, alpha=0.5)
        plt.legend()
        plt.show()
# speech to text model


def speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# Linear Regression visualisation Model


class LinearCorrelationVisualizer:
    def __init__(self, stock_a, stock_b):
        self.stock_a = stock_a
        self.stock_b = stock_b

    def visualize(self):
        days = 365*2
        stock_data_a = Stock(self.stock_a).price().tail(days)
        stock_data_b = Stock(self.stock_b).price().tail(days)
        x = stock_data_a['Close'].values
        y = stock_data_b['Close'].values
        lm = LinearModel()
        slope, intercept = lm.LinearRegression(x, y)
        trend = "Upward Trend" if slope > 0 else "Downward Trend" if slope < 0 else "Flat"
        print(f"Trend: {trend}")
        print(f"Slope: {slope}")
        print(f"Intercept: {intercept}")
        y_pred = [intercept + slope * xi for xi in x]
        obj3 = Plot(x, y)
        obj3.ScatterPlot(x, y_pred)
        speech_text = f"The linear model for correlation analysis between {self.stock_a} and {self.stock_b} is showing {trend}."
        speech(speech_text)
