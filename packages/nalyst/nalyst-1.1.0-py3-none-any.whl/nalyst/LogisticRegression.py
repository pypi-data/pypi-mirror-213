from typing import List, Tuple


class LogisticRegression:
    """
    Class for building and analyzing a logistic regression model.

    Attributes:
        x (List[float]): List of x values.
        y (List[float]): List of y values.
        learning_rate (float): Learning rate for the gradient descent algorithm.
        iterations (int): Number of iterations for the gradient descent algorithm.
        weights (List[float]): List of weights for each feature.

    Methods:
        sigmoid(z: float) -> float: Compute the sigmoid function.
        predict(x: List[float]) -> List[float]: Generate predicted y values based on a list of x values.
        train() -> None: Train the logistic regression model using gradient descent.
    """

    def __init__(self, x: List[float], y: List[float], learning_rate: float = 0.01, iterations: int = 1000):
        """
        Initialize the LogisticRegressionModel class.

        Args:
            x (List[float]): List of x values.
            y (List[float]): List of y values.
            learning_rate (float): Learning rate for the gradient descent algorithm.
            iterations (int): Number of iterations for the gradient descent algorithm.
        """
        self.x = x
        self.y = y
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = [0] * (len(x[0]) + 1)

    def sigmoid(self, z: float) -> float:
        """
        Compute the sigmoid function.

        Args:
            z (float): Input to the sigmoid function.

        Returns:
            float: Output of the sigmoid function.
        """
        return 1 / (1 + pow(2.71828, -z))

    def predict(self, x: List[float]) -> List[float]:
        """
        Generate predicted y values based on a list of x values.

        Args:
            x (List[float]): List of x values.

        Returns:
            List[float]: List of predicted y values.
        """
        y_pred = []
        for i in range(len(x)):
            z = self.weights[0]
            for j in range(len(x[i])):
                z += self.weights[j+1] * x[i][j]
            y_pred.append(self.sigmoid(z))
        return y_pred

    def train(self) -> None:
        """
        Train the logistic regression model using gradient descent.
        """
        for iteration in range(self.iterations):
            gradient = [0] * len(self.weights)
            for i in range(len(self.x)):
                z = self.weights[0]
                for j in range(len(self.x[i])):
                    z += self.weights[j+1] * self.x[i][j]
                h = self.sigmoid(z)
                gradient[0] += (h - self.y[i])
                for j in range(len(self.x[i])):
                    gradient[j+1] += (h - self.y[i]) * self.x[i][j]
            for j in range(len(self.weights)):
                self.weights[j] -= self.learning_rate * gradient[j]


def accuracy(y_true: List[float], y_pred: List[float]) -> float:
    """
    Calculate the accuracy of the logistic regression model.

    Args:
        y_true (List[float]): List of actual y values.
        y_pred (List[float]): List of predicted y values.

    Returns:
        float: Accuracy of the logistic regression model.
    """
    correct = 0
    for i in range(len(y_true)):
        if y_pred[i] >= 0.5:
            if y_true[i] == 1:
                correct += 1
        else:
            if y_true[i] == 0:
                correct += 1
    return correct / len(y_true)
