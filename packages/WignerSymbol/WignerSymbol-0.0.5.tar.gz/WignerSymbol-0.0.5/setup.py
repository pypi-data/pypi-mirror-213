from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

__version__ = "0.0.5"

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
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires='>=3.6',
)
