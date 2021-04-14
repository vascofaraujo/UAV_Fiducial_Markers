from setuptools import setup, Extension

setup(
    name='helloWorld',
    version='1.0',
    description='Python Package with Hello World C++ Extension',
    ext_modules=[
        Extension(
            'helloWorld',
            sources=['pyboostcvconverter/pyboost_cv3_converter.cpp', 'hello_worldmodule.cpp'],
            include_dirs=['/usr/lib/python3/dist-packages/numpy/'],
            libraries=['opencv_core', 'opencv_highgui', 'opencv_videoio'],
            py_limited_api=True)
    ],
)
