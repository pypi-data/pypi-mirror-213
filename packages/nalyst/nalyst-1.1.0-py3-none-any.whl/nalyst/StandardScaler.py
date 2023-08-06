from typing import List, Tuple


class StandardScaler:
    """
    Standardize features by removing the mean and scaling to unit variance.

    Attributes:
        mean_ (list): Mean of each feature.
        scale_ (list): Standard deviation of each feature.

    Methods:
        fit(X: List[List[float]]) -> StandardScaler: Compute the mean and standard deviation of each feature.
        transform(X: List[List[float]]) -> List[List[float]]: Standardize the data by removing the mean and scaling to unit variance.
        fit_transform(X: List[List[float]]) -> List[List[float]]: Compute the mean and standard deviation of each feature, and standardize the data.
    """

    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X: List[List[float]]) -> 'StandardScaler':
        """
        Compute the mean and standard deviation of each feature.

        Args:
            X (list of lists): Input data.

        Returns:
            StandardScaler: The fitted StandardScaler object.
        """
        n_features = len(X[0])
        n_samples = len(X)
        self.mean_ = [0] * n_features
        self.scale_ = [0] * n_features
        for j in range(n_features):
            sum_x = 0
            sum_sq_x = 0
            for i in range(n_samples):
                sum_x += X[i][j]
                sum_sq_x += X[i][j]**2
            mean = sum_x / n_samples
            self.mean_[j] = mean
            self.scale_[j] = ((sum_sq_x / n_samples) - (mean**2))**0.5
        return self

    def transform(self, X: List[List[float]]) -> List[List[float]]:
        """
        Standardize the data by removing the mean and scaling to unit variance.

        Args:
            X (list of lists): Input data.

        Returns:
            list of lists: The standardized data.
        """
        X_std = [[0] * len(row) for row in X]
        for j in range(len(X[0])):
            for i in range(len(X)):
                X_std[i][j] = (X[i][j] - self.mean_[j]) / self.scale_[j]
        return X_std

    def fit_transform(self, X: List[List[float]]) -> List[List[float]]:
        """
        Compute the mean and standard deviation of each feature, and standardize the data.

        Args:
            X (list of lists): Input data.

        Returns:
            list of lists: The standardized data.
        """
        self.fit(X)
        X_std = self.transform(X)
        return X_std
