import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

def main():
    results = []
    for k in range (1,11):
        data = load_iris().data
        algo = KMeans(n_clusters = k ,init='k-means++', n_init='auto', max_iter=300, tol=0.0001, random_state=0).fit(data)
        inertia = algo.inertia_
        results.append((k, inertia))
    x_coordinates, y_coordinates = zip(*results)
    max_inertia = max(y_coordinates)
    fig, ax = plt.subplots()
    ax.set_xlim(0, 9)
    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_ylim(0, 3)
    ax.set_yticks(np.arange(0, max_inertia * 1.15, 100))
    ax.set_title('Elbow Method for selection of optimal "K" clusters')
    ax.set_xlabel("K")
    ax.set_ylabel("Average Dispersion")
    ax.plot(x_coordinates, y_coordinates, marker='o', linestyle='-', color='blue')

if __name__ == '__main__':
    main()
    plt.savefig('elbow.png')
    plt.show()
