from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("libcythonconst.lsum", ["libcythonconst/lsum.pyx"])]

setup(
    name="Library package with const in Cython",
    ext_modules=cythonize(extensions),
    include_package_data=True,
    package_data={'libcythonconst': ['lsum.pyx', 'lsum.pxd', 'lsum.h']},
    zip_safe=False,
)
