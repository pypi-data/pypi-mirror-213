
from typing import List, Tuple
import random


class TrainTestSplit:
    """
    Class for splitting data into training and test sets.

    Attributes:
        X (list): Feature matrix.
        y (list): Target array.
        test_size (float): Proportion of the data to use for the test set.

    Methods:
        split() -> Tuple[list]: Split the data into training and test sets.
    """

    def __init__(self, X: list, y: list, test_size: float = 0.2):
        """
        Initialize the TrainTestSplit class.

        Args:
            X (list): Feature matrix.
            y (list): Target array.
            test_size (float, optional): Proportion of the data to use for the test set. Defaults to 0.2.
        """
        self.X = X
        self.y = y
        self.test_size = test_size

    def split(self) -> Tuple[list]:
        """
        Split the data into training and test sets.

        Returns:
            Tuple[list]: Tuple containing the training and test sets of the feature matrix and target array.
        """
        # Set the random seed to 0 for reproducibility
        random.seed(0)

        # Shuffle the indices of the data
        indices = list(range(len(self.X)))
        random.shuffle(indices)

        # Split the indices into training and test indices based on the test size
        split = int(len(self.X) * (1-self.test_size))
        train_indices = indices[:split]
        test_indices = indices[split:]

        # Split the data into training and test sets
        X_train = [self.X[i] for i in train_indices]
        y_train = [self.y[i] for i in train_indices]
        X_test = [self.X[i] for i in test_indices]
        y_test = [self.y[i] for i in test_indices]

        return X_train, X_test, y_train, y_test
