import matplotlib.pyplot as plt
import numpy as np
from typing import List


class RegressionPlot:
    def residual_plot(self):
        """
        Plot the residual plot of the linear regression model.
        """
        plt.style.use("dark_background")
        plt.figure(figsize=(15, 6))

        X = np.array(self.x).flatten()
        y = np.array(self.y).flatten()
        y_pred = np.array(self.predict(self.x)).flatten()

        residuals = y - y_pred
        above_line = X[np.where(residuals >= 0)]
        below_line = X[np.where(residuals < 0)]
        y_above_line = y[np.where(residuals >= 0)]
        y_below_line = y[np.where(residuals < 0)]

        plt.scatter(above_line, y_above_line, color="red",
                    alpha=0.5, label="Above best-fit line")
        plt.scatter(below_line, y_below_line, color="white",
                    alpha=0.5, label="Below best-fit line")
        plt.plot(X, y_pred, color="yellow", label="Best-fit line")

        min_residual_idx = np.argmin(np.abs(residuals))
        max_residual_idx = np.argmax(np.abs(residuals))

        plt.annotate(
            f"Nearest residual: {residuals[min_residual_idx]:.2f}",
            (X[min_residual_idx], y[min_residual_idx]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            color="cyan",
        )

        plt.annotate(
            f"Largest residual: {residuals[max_residual_idx]:.2f}",
            (X[max_residual_idx], y[max_residual_idx]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            color="magenta",
        )

        plt.grid(linestyle='--', color='gray', alpha=0.8)
        plt.title("Residual Plot")
        plt.ylabel("Dependent variable")
        plt.xlabel("Independent variable")
        plt.legend()
        plt.show()
        plt.close()
