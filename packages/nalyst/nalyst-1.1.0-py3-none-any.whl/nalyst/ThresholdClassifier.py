import matplotlib.pyplot as plt
import numpy as np
from typing import List


class ThresholdClassifier:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def classify(self, data: List[float]):
        self.mean = sum(data) / len(data)
        self.threshold = self.mean
        classifications = []
        for value in data:
            if value > self.threshold:
                classifications.append(1)
            else:
                classifications.append(0)
        return classifications


class ThresholdPlot:
    def __init__(self, data, classification):
        self.data = data
        self.classification = classification

    def plot(self):
        plt.style.use('dark_background')
        plt.figure(figsize=(30, 7))
        plt.xlabel("Time", fontsize=14)
        plt.ylabel("Price (£)", color="tab:red", fontsize=14)
        plt.plot(self.data.index, self.data, color="tab:red")
        plt.twinx()
        plt.ylabel("Classification", color="tab:blue", fontsize=14)
        plt.plot(self.data.index, self.classification, color="tab:blue")
        plt.axhline(y=0.5, color="gray", linestyle="--", alpha=0.8)
        plt.title("Binary Classifications", fontsize=20, color="White")
        plt.grid(linestyle='--', color='gray', alpha=0.2)
        plt.show()

        colors = []
        for value in self.classification:
            if value > 0.5:
                colors.append("tab:green")
            else:
                colors.append("tab:red")

        plt.style.use('dark_background')
        plt.figure(figsize=(30, 7))
        plt.xlabel("Time", fontsize=14)
        plt.ylabel("Price (£)", color="tab:red", fontsize=14)
        plt.plot(self.data.index, self.data, color="tab:red")
        plt.tick_params(axis="both", labelsize=12)
        plt.twinx()
        plt.ylabel("Classification", color="tab:blue", fontsize=14)
        plt.scatter(self.data.index, self.classification, color=colors)
        plt.tick_params(axis="both", labelsize=12)
        plt.title("Binary Classifications", fontsize=18, color="White")
        plt.grid(linestyle='--', color='gray', alpha=0.2)
        plt.show()
