import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as patch
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

def main():
    results = []
    data = load_iris().data
    for k in range (1,11):
        algo = KMeans(n_clusters = k ,init='k-means++', n_init='auto', max_iter=300, tol=0.0001, random_state=0).fit(data)
        inertia = algo.inertia_
        results.append((k, inertia))
    x_coordinates, y_coordinates = zip(*results)
    max_point = np.array([0, y_coordinates[0]])
    min_point = np.array([9, y_coordinates[9]])
    max_distance = 0
    max_k = 1
    
    for k in range (0,10):
        curr_point = np.array([x_coordinates[k], y_coordinates[k]])
        v1 = np.append(max_point - curr_point, 0)
        v2 = np.append(max_point - min_point, 0)
        curr_distance = np.linalg.norm(np.cross(v1, v2)) / np.linalg.norm((v2))
        if curr_distance > max_distance:
            max_distance = curr_distance
            max_k_index = k
            max_k = x_coordinates[k]

    max_inertia = y_coordinates[max_k_index]                                               
    fig, ax = plt.subplots()
    ax.set_xlim(0, None)
    ax.set_xticks(np.arange(0, 11.5, 1))
    ax.set_ylim(min(y_coordinates) * 0.95, max(y_coordinates) * 1.05)
    font1 = {'family':'serif','color':'red','size': 14, 'style': 'italic'}
    font2 = {'family':'serif','color':'red','size': 10, 'style': 'italic'}
    ax.set_title('Elbow Method for selection of optimal "K" clusters', fontdict = font1)
    ax.set_xlabel("K", fontdict=font2)
    ax.set_ylabel("Average Dispersion", fontdict=font2)
    ax.plot(x_coordinates, y_coordinates, linestyle='-', color='blue', label='Inertia Plot')
    elbow_x = max_k
    elbow_y = max_inertia
    ax.plot(elbow_x, elbow_y, marker='o', color='red', markersize=24, markerfacecolor='none', linestyle='none', label='Elbow')

    ax.annotate('                                                               ',
        xy=(elbow_x * 1.15, elbow_y * 1.15),
        arrowprops=dict(arrowstyle='-|>', color='black', lw=2),
        color='black',
        ha='left'
    )

    ax.grid()
    ax.legend(fontsize=14)
    plt.savefig('elbow.png')
    plt.show()
   
if __name__ == '__main__':
    main()