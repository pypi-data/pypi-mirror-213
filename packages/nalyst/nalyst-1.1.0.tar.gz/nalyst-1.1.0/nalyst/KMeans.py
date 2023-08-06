import random


class KMeans:
    def __init__(self, n_clusters, max_iter=300):
        """
        Initialize the KMeans class.

        Args:
            n_clusters (int): Number of clusters.
            max_iter (int, optional): Maximum number of iterations. Defaults to 300.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def euclidean_distance(self, a, b):
        """
        Compute the Euclidean distance between two points.

        Args:
            a (list): First point.
            b (list): Second point.

        Returns:
            float: Euclidean distance.
        """
        distance = 0
        for i in range(len(a)):
            distance += (a[i] - b[i])**2
        return distance ** 0.5

    def fit(self, X):
        """
        Fit the KMeans model to the data.

        Args:
            X (list): Feature matrix.

        Returns:
            None.
        """
        self.centroids = random.sample(X, self.n_clusters)
        for i in range(self.max_iter):
            clusters = [[] for _ in range(self.n_clusters)]
            for x in X:
                distances = [self.euclidean_distance(
                    x, c) for c in self.centroids]
                closest_cluster = distances.index(min(distances))
                clusters[closest_cluster].append(x)
            old_centroids = self.centroids[:]
            for i in range(self.n_clusters):
                self.centroids[i] = [sum(column) / len(clusters[i])
                                     for column in zip(*clusters[i])]
            if self.centroids == old_centroids:
                break

    def predict(self, X):
        """
        Predict the cluster labels for new data.

        Args:
            X (list): Feature matrix.

        Returns:
            list: Predicted cluster labels.
        """
        predictions = []
        for x in X:
            distances = [self.euclidean_distance(x, c) for c in self.centroids]
            closest_cluster = distances.index(min(distances))
            predictions.append(closest_cluster)
        return predictions
