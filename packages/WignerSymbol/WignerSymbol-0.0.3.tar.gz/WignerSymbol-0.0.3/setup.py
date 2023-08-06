from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.3"

ext_modules = [
    Pybind11Extension("WignerSymbol",
                      ["lib.cpp"],
                      define_macros=[("VERSION", __version__)]
                      ),
]

setup(
    name='WignerSymbol',
    version=__version__,
    author="0382",
    author_email="18322825326@163.com",
    url="https://github.com/0382/WignerSymbol-pybind11",
    description="Python port of 0382/WignerSymbol",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
