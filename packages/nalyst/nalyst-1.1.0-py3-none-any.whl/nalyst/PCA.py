import numpy as np


class PCA:
    """
    Principal Component Analysis (PCA) is a technique used for reducing the dimensionality of data.

    Attributes:
        n_components (int): Number of principal components to keep.

    Methods:
        fit_transform(X: ndarray) -> ndarray: Fit the PCA model and apply the dimensionality reduction to the data.
    """

    def __init__(self, n_components: int = None):
        """
        Initialize the PCA class.

        Args:
            n_components (int, optional): Number of principal components to keep. Defaults to None.
        """
        self.n_components = n_components

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Fit the PCA model and apply the dimensionality reduction to the data.

        Args:
            X (ndarray): Input data.

        Returns:
            ndarray: Transformed data with reduced dimensionality.
        """
        # Center the data
        X_centered = X - np.mean(X, axis=0)

        # Compute the covariance matrix
        cov_matrix = np.cov(X_centered.T)

        # Compute the eigenvalues and eigenvectors of the covariance matrix
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

        # Sort the eigenvalues and eigenvectors in descending order
        indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[indices]
        eigenvectors = eigenvectors[:, indices]

        # Choose the number of components to keep
        if self.n_components is None:
            self.n_components = X.shape[1]
        else:
            self.n_components = min(self.n_components, X.shape[1])

        # Select the top k eigenvectors
        top_eigenvectors = eigenvectors[:, :self.n_components]

        # Project the data onto the top k eigenvectors
        X_reduced = np.dot(X_centered, top_eigenvectors)

        return X_reduced
