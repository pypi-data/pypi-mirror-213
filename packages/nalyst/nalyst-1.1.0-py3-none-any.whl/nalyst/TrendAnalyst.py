import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyttsx3
import seaborn as sns
import yfinance as yf
import datetime


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


def linear_regression_trend(x, y):
    lm = LinearModel()
    slope, intercept = lm.LinearRegression(x, y)
    if slope > 0:
        trend = "Upward Trend"
    elif slope < 0:
        trend = "Downard Trend"
    else:
        trend = "flat"
    return slope, intercept, trend


def plot_regression(x, y, slope, intercept):
    y_pred = [intercept + slope * xi for xi in x]
    # Convert the ordinal date values back to datetime format
    x_dates = [datetime.datetime.fromordinal(int(d)) for d in x]
    plt.style.use('dark_background')
    plt.figure(figsize=(15, 6))
    plt.plot(x_dates, y, label="Actual", color="red", alpha=0.9)
    plt.plot(x_dates, y_pred, color="orange", linewidth=2, label="Predicted")
    plt.grid(color='white', linestyle='--', linewidth=1, alpha=0.5)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel(f"Close Price", fontsize=14)
    plt.title("Trend Analysis", fontsize=18)
    plt.legend(fontsize=12)
    plt.rcParams['axes.facecolor'] = '#f9f9f9'
    plt.show()


def speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()


class LinearRegressionVisualizer:
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date

    def visualize(self):
        days = 365*2
        stock_data = yf.download(
            self.stock.upper(), start=self.start_date, end=self.end_date)
        stock_data = stock_data[['Close']].tail(days)
        stock_data['Date'] = [d.date().toordinal() for d in stock_data.index]
        x = stock_data['Date'].values
        y = stock_data.Close.values
        slope, intercept, trend = linear_regression_trend(x, y)
        print(f"Slope: {slope}")
        print(f"Intercept: {intercept}")
        print(f"Trend: {trend}")
        y_pred = [intercept + slope * xi for xi in x]
        plot_regression(x, y, slope, intercept)
        speech_text = f"The linear model for trend analysis of {self.stock} from {self.start_date} to {self.end_date} is showing{trend}."
        speech(speech_text)
