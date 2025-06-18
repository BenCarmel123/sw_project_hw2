#define _GNU_SOURCE
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double euclideanDist(double* x, double*y, int dim) { /* Calculate Euclidean distance between 2 Vectors */
    double sum = 0.0;
    int i;
    for (i = 0; i < dim; i++)
    {
        sum += pow(x[i] - y[i], 2);
    }
    return sqrt(sum);
}

int calcMin(double* x, double** centroids, int k, int dim) /* Find the closest centroid to Vector X */
{
    int minIndex = 0;
    double minDist = euclideanDist(x, centroids[0], dim);
    int i;
    for (i = 1; i < k; i++)
    {
        double dist = euclideanDist(x, centroids[i], dim);
        if (dist < minDist) {
            minDist = dist;
            minIndex = i;
        }
    }
    return minIndex;
}

void assignClusters(double** vectors, int numVectors, double** centroids, int k, int dim, double**** clustersOut, int** clusterSizesOut) 
/* Derive new clusters from centroids*/
{
    double*** clusters;
    int* clusterSizes;
    int* clusterCaps;
    int i;
    int v;
    clusters = malloc(k * sizeof(double**)); /* Denote a list with k bins which all contain all relevant vectors to the cluster*/
    clusterSizes = calloc(k, sizeof(int));
    clusterCaps = malloc(k * sizeof(int));
    
    for (i = 0; i < k; i++) 
    {
        clusterCaps[i] = 10;
        clusters[i] = malloc(clusterCaps[i] * sizeof(double*));
    }

    for (v = 0; v < numVectors; v++) /* Find closest Vectors*/
    {
        int closest;
        closest = calcMin(vectors[v], centroids, k, dim);

        if (clusterSizes[closest] >= clusterCaps[closest]) 
        {
            clusterCaps[closest] *= 2;
            clusters[closest] = realloc(clusters[closest], clusterCaps[closest] * sizeof(double*));
        }

        clusters[closest][clusterSizes[closest]++] = vectors[v];
    }

    *clustersOut = clusters;
    *clusterSizesOut = clusterSizes;

    free(clusterCaps);
}

double* newCentr(double** cluster, int size, int dim) { /* Calculate the new Average (Centroid value) after assignments */
    int i, j;
    double* centroid;
    double* new_centroid;
    if (size < 2) { /* If there is only one vector return it*/
        centroid = malloc(dim * sizeof(double));
        for (i = 0; i < dim; i++) {
            centroid[i] = cluster[0][i];
        }
        return centroid;
    }

    /* Allocate new centroid */
    new_centroid = calloc(dim, sizeof(double)); /* denote with zeros */

    for (i = 0; i < dim; i++) { /* For each 'intro' of the vector calc the new average */
        for (j = 0; j < size; j++) {
            new_centroid[i] += cluster[j][i];
        }
        new_centroid[i] /= size;
    }

    return new_centroid; /* Return the new centroid according to new vectors assignment*/
}

int has_converged(double** old_centroids, double** new_centroids, int k, int dim) {
    int i;
    for (i = 0; i < k; i++) {
        if (euclideanDist(old_centroids[i], new_centroids[i], dim) >= 0.001) {
            return 0;
        }
    }
    return 1;
}

int updateCentr(double*** clusters, int* clusterSizes, double*** centroids, int k, int dim) {
    /* Update centroids according to new clusters */
    double** old_centroids;
    double** new_centroids;
    int i;
    int flag;
    old_centroids = *centroids;
    new_centroids = malloc(k * sizeof(double*)); /* Allocate memory for new centroids */

    for (i = 0; i < k; i++) { /* For each cluster calculate the new centroid */
        new_centroids[i] = newCentr(clusters[i], clusterSizes[i], dim);
    }

    flag = !has_converged(old_centroids, new_centroids, k, dim); /* Check if the centroids have converged */

    for (i = 0; i < k; i++) { /* Free old centroids */
        free(old_centroids[i]);
    }
    free(old_centroids);
    *centroids = new_centroids;

    return flag;
}

static double** convertPythonToC(PyObject *python_data, int *num_of_vectors, int *dimension) {
    /* Convert Python list of lists to C double array */
    PY_ssize_t i, k, j;
    Py_ssize_t size = PyList_Size(python_data);
    *num_of_vectors = (int)size;
    *dimension = (int)PyList_Size(PyList_GetItem(python_data, 0));

    /* Allocate memory */
    double **c_array = (double **)malloc(size * sizeof(double*));
    if (c_array == NULL) {
        printf("Memory allocation failed.\n");
        exit(1);
    }

    for (i = 0; i < size; i++) {
        PyObject *row = PyList_GetItem(python_data, i);

        /* Allocate memory for each vector */
        c_array[i] = (double *)malloc(*dimension * sizeof(double));
        if (c_array[i] == NULL) {
            printf("Memory allocation failed.\n");
            // Free previously allocated rows
            for (k = 0; k < i; k++) free(c_array[k]);
            free(c_array);
            exit(1);
        }

        for (j = 0; j < *dimension; j++) {
            c_array[i][j] = PyFloat_AsDouble(PyList_GetItem(row, j));
        }
    }
    return c_array;
}

PyObject* convertCToPython(double **c_array, int num_of_vectors, int dimension) {
    /* Convert C double array to Python list of lists */
    int i, j;
    PyObject *python_list = PyList_New(num_of_vectors);
    for (i = 0; i < num_of_vectors; i++) {
        PyObject *item = PyList_New(dimension);
        for (j = 0; j < dimension; j++) {
            PyList_SetItem(item, j, PyFloat_FromDouble(c_array[i][j]));
        }
        PyList_SetItem(python_list, i, item);
    }
    return python_list;
}

PyObject* runKmeans(int k, int iter, double epsilon, PyObject *python_data, PyObject *python_centroids) {
    /* Main function to run K-means algorithm */
    int converged = 0, dimension = 0, num_of_vectors = 0, i, current_iter;
    double*** clusters;
    double** centroids, **vectors;
    int* clusterSizes;

    vectors = convertPythonToC(python_data, &num_of_vectors, &dimension); 
    centroids = convertPythonToC(python_centroids, &k, &dimension); 

    for (current_iter = 0; current_iter < iter; current_iter++) {
        assignClusters(vectors, num_of_vectors, centroids, k, dimension, &clusters, &clusterSizes); /* Use centroids to assign Cluster */
        converged = updateCentr(clusters, clusterSizes, &centroids, k, dimension); /* Check if converged and update Centroids */

        for (i = 0; i < k; i++) { /* Free clusters */
            free(clusters[i]);
        }
        free(clusters);
        free(clusterSizes);

        if (!converged) break; /* Break the loop if centroids have converged */
    }
    
    final_centroids = convertCToPython(centroids, k, dimension); /* Convert final centroids back to Python */

    for (i = 0; i < k; i++) { /* Free centroids */
        free(centroids[i]);
    }
    free(centroids);

    for (i = 0; i < num_of_vectors; i++) { /* Free vectors */
        free(vectors[i]);
    }
    free(vectors);

    return final_centroids; /* Return final centroids as Python object */
}