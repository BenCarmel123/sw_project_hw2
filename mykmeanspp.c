#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* fit(PyObject* self, PyObject *args)
{
    int k;
    int iter; 
    double epsilon;
    PyObject *data = NULL;
    PyObject *initial_centroids = NULL;

    if(!PyArg_ParseTuple(args, "iidOO", &k, &iter, &epsilon, &data ,&initial_centroids)) 
    {
        return NULL; 
    }
    
    return Py_BuildValue("O", runKmeans(k, iter, epsilon, data, initial_centroids))
}

static PyMethodDef kmeansMethods[] = {
    {"fit",                  
      (PyCFunction) fit, 
      METH_VARARGS,          
      PyDoc_STR(NULL)}, 
    {NULL, NULL, 0, NULL}     
};

static struct PyModuleDef kmeansModule = {
    PyModuleDef_HEAD_INIT,
    "mykmeanspp", 
    NULL, 
    -1, 
    kmeansMethods 
};

PyMODINIT_FUNC PyInit_mykmeanspp(void)
{
    PyObject *m;
    m = PyModule_Create(&kmeansModule);
    if (!m) {
        return NULL;
    }
    return m;
};