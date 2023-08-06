from sklearn.cluster import KMeans
import abc
import numpy as np

class IKmeans:
    @abc.abstractmethod
    def fit(self, data=[]) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict(self) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict_cluster(self) -> object:
        raise NotImplementedError
    
class KMeansMov_2(IKmeans):
    def __init__(self, n_clusters=4, max_iter=300):
        self.kmean = KMeans(n_clusters=n_clusters, n_init=10, random_state=0, max_iter=max_iter, tol=1e-4)
        self.range_threshold = 1.5
        self.kmean_ev = None

    def fit(self, X):
        self.kmean_ev = self.kmean.fit(X)

    def predict(self, X):
        distances = self.kmean_ev.transform(X)
        closest_cluster_distance = np.min(distances, axis=1)
        return [1 if closest_cluster_distance[0] <= self.range_threshold else 0]
    
    def predict_cluster(self, X):
        return self.kmean_ev.predict(X)


class KMeansNov_2(IKmeans):
    def __init__(self, n_clusters=4, max_iter=300):
        self.kmean = KMeans(n_clusters=n_clusters, n_init=10, random_state=0, max_iter=max_iter, tol=1e-4)
        self.range_threshold = 0.90
        self.kmean_ev = None

    def fit(self, X):
        self.kmean_ev = self.kmean.fit(X)

    def predict(self, X):
        distances = self.kmean_ev.transform(X)
        closest_cluster_distance = np.min(distances, axis=1)
        return [1 if closest_cluster_distance[0] <= self.range_threshold else 0]
    
    def predict_cluster(self, X):
        return self.kmean_ev.predict(X)
    
