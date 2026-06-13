from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "markowitz_cpp",
        ["markowitz.cpp"],
        include_dirs=["C:/Users/praxy/Downloads/eigen-5.0.0"],
    ),
]

setup(
    name="markowitz_cpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)