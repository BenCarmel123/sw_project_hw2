#include <Python.h>

# ifndef KMEANS_H_
# define KMEANS_H_

PyObject* runKmeans(int k, int iter, double epsilon, PyObject *data, PyObject *initial_centroids);

# endif