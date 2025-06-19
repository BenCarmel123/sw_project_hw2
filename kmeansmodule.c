#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "kmeans.h"

    /*

    An implementaion of 'fit()' function 
    -------------------------------------
    PyObject -> C Array Object -> PyObject
    fit() receives k initial centroids and the dataset and returns k clusters.

    Parameters
    ----------
    2
    k : int
        -- Desired number of clusters 

    iter : int 
        -- Number of maximum iterations 

    epsilon : float -> double
        -- Covergence parameter

    data : PyObject -> float[][] -> PyObject
        -- Provided dataset

    initial_centroids : PyObject -> float[][] -> PyObject
        -- Initial centroids after step 1 of kmeans++ algorithm

    Returns
    -------
    PyObject
        -- Returns final K clusters 

    */

/* A function that parses the arguments to their C counterparts */
static PyObject* fit(PyObject *self, PyObject *args)
{
    int k;
    int iter; 
    double epsilon;
    PyObject *data = NULL;
    PyObject *initial_centroids = NULL;

    if(!PyArg_ParseTuple(args, "iidOO", &k, &iter, &epsilon, &data ,&initial_centroids)) 
    {
        return NULL; /*  Returns NULL if an error has occured  */
    }
    
    return Py_BuildValue("O", runKmeans(k, iter, epsilon, data, initial_centroids)); /* Converts the result computed in the C file back to a generic PyObject */
};

static PyMethodDef kmeansMethods[] = { /* Description of all methods to execute in c */
    {"fit",                  
      (PyCFunction) fit, /* In our case, it's only fit() */
      METH_VARARGS,          
      PyDoc_STR("A function that runs the Kmeans clustering algorithm without initializing centroids")}, 
    {NULL, NULL, 0, NULL}     
};

static struct PyModuleDef mykmeansModule = { /* Module definition */
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", 
    NULL, 
    -1, 
    kmeansMethods 
};

PyMODINIT_FUNC PyInit_mykmeanspp(void) /* Init function */
{
    PyObject *m;
    m = PyModule_Create(&mykmeansModule);
    if (!m) {
        return NULL;
    }
    return m;
};