import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as patch
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
    ax.set_xlim(0, None)
    ax.set_xticks(np.arange(0, 11.5, 1))
    ax.set_ylim(0, None)
    ax.set_yticks(np.arange(0, max_inertia * 1.15, 100))
    font1 = {'family':'serif','color':'red','size': 14, 'style': 'italic'}
    font2 = {'family':'serif','color':'red','size': 10, 'style': 'italic'}
    ax.set_title('Elbow Method for selection of optimal "K" clusters', fontdict = font1)
    ax.set_xlabel("K", fontdict=font2)
    ax.set_ylabel("Average Dispersion", fontdict=font2)
    ax.plot(x_coordinates, y_coordinates, linestyle='-', color='blue', label='Inertia Plot')
    elbow = (3,results[2][1])
    ax.grid()
    ax.legend(['Inertia Plot', 'Elbow'])
if __name__ == '__main__':
    main()
    plt.savefig('elbow.png')
    plt.show()
