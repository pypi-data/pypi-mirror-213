from typing import List, Tuple


class MaxAbsScaler:
    """
    Scale features by their maximum absolute value.

    Attributes:
        max_abs_ (List[float]): Maximum absolute value for each feature.

    Methods:
        fit(data: List[List[float]]) -> None: Compute the maximum absolute value for each feature.
        transform(data: List[List[float]]) -> List[List[float]]: Scale the data by its maximum absolute value.
        fit_transform(data: List[List[float]]) -> List[List[float]]: Compute the maximum absolute value for each feature and scale the data by its maximum absolute value.
    """

    def __init__(self):
        pass

    def fit(self, data: List[List[float]]) -> None:
        """
        Compute the maximum absolute value for each feature.

        Args:
            data (List[List[float]]): Input data.

        Returns:
            None.
        """
        self.max_abs_ = [max(map(abs, col)) for col in zip(*data)]

    def transform(self, data: List[List[float]]) -> List[List[float]]:
        """
        Scale the data by its maximum absolute value.

        Args:
            data (List[List[float]]): Input data.

        Returns:
            List[List[float]]: Scaled data.
        """
        scaled = [[value / max_abs for value,
                   max_abs in zip(row, self.max_abs_)] for row in data]
        return scaled

    def fit_transform(self, data: List[List[float]]) -> List[List[float]]:
        """
        Compute the maximum absolute value for each feature and scale the data by its maximum absolute value.

        Args:
            data (List[List[float]]): Input data.

        Returns:
            List[List[float]]: Scaled data.
        """
        self.fit(data)
        return self.transform(data)
