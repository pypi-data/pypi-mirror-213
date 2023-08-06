class MinMaxScaler:
    """
    Class for scaling data using MinMaxScaler.

    Attributes:
        feature_range (tuple): The feature range to scale the data to (default: (0, 1)).
        min_ (numpy.ndarray): The minimum values of each feature.
        max_ (numpy.ndarray): The maximum values of each feature.
        scale_ (numpy.ndarray): The scaling factor of each feature.
        min_scaled_ (numpy.ndarray): The scaled minimum values of each feature.

    Methods:
        fit(data: numpy.ndarray) -> None: Compute the minimum and maximum values of each feature.
        transform(data: numpy.ndarray) -> numpy.ndarray: Scale the data based on the fitted values.
        fit_transform(data: numpy.ndarray) -> numpy.ndarray: Fit to the data, then transform it.
    """

    def __init__(self, feature_range=(0, 1)):
        """
        Initialize the MinMaxScaler class.

        Args:
            feature_range (tuple, optional): The feature range to scale the data to (default: (0, 1)).
        """
        self.feature_range = feature_range

    def fit(self, data):
        """
        Compute the minimum and maximum values of each feature.

        Args:
            data (numpy.ndarray): The data to fit the scaler on.
        """
        self.min_ = data.min(axis=0)
        self.max_ = data.max(axis=0)
        self.scale_ = (
            self.feature_range[1] - self.feature_range[0]) / (self.max_ - self.min_)
        self.min_scaled_ = self.feature_range[0] - self.min_ * self.scale_

    def transform(self, data):
        """
        Scale the data based on the fitted values.

        Args:
            data (numpy.ndarray): The data to scale.

        Returns:
            numpy.ndarray: The scaled data.
        """
        scaled = data * self.scale_ + self.min_scaled_
        return scaled

    def fit_transform(self, data):
        """
        Fit to the data, then transform it.

        Args:
            data (numpy.ndarray): The data to fit and scale.

        Returns:
            numpy.ndarray: The fitted and scaled data.
        """
        self.fit(data)
        return self.transform(data)
