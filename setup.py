from setuptools import Extension, setup
module = Extension("mykmeanspp", sources=['kmeansmodule.c', 'kmeans.c'])
setup(name='mykmeanspp',
     version='1.0',
     description='Kmeans C extension Python wrapper',
     ext_modules=[module])