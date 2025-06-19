import numpy as np 
import matplotlib as plt 
from kmeanspp import func
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

def main():
    for k in range (1,11):
        data = load_iris().data
        algo = KMeans(n_clusters = k ,init='kmeanspp', n_init='auto', max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='lloyd').fit(data)
        inertia = algo.inertia_

if __name__ == '__main__':
    main()