from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "markowitz_cpp",
        ["markowitz.cpp"],
        include_dirs=["/usr/include/eigen3"],
    ),
]

setup(
    name="markowitz_cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)