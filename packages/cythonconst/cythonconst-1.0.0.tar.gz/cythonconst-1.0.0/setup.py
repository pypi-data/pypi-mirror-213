from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("cythonconst.plus", ["cythonconst/plus.pyx"])]

setup(
    name="Client package with const in Cython",
    ext_modules=cythonize(extensions),
    include_package_data=True,
    package_data={'cythonconst': ['plus.pyx']},
    zip_safe=False,
)