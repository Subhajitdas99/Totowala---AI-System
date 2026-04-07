import numpy as np
from sklearn.cluster import KMeans
import math

def cluster_passengers(passengers, max_per_vehicle=4):
    if len(passengers) == 0:
        return []

    coords = np.array([[p['lat'], p['lon']] for p in passengers])

    n_clusters = math.ceil(len(passengers) / max_per_vehicle)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    labels = kmeans.fit_predict(coords)

    groups = {}
    for i, label in enumerate(labels):
        groups.setdefault(label, []).append(passengers[i])

    return list(groups.values())