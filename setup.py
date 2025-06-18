from setuptools import Extension, setup

module = Extension("kmeanshelper", sources=['kmeansmodule.c', 'kmeans.c'])
setup(name='kmeanshelper',
     version='1.0',
     description='Python wrapper for kmeans C extension',
     ext_modules=[module])