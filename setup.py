import sys
import numpy
from setuptools import setup, Extension

# LAPACK linking: Accelerate on macOS, liblapack on Linux
if sys.platform == "darwin":
    lapack_libs = []
    lapack_link = ["-framework", "Accelerate"]
else:
    lapack_libs = ["lapack"]
    lapack_link = []

oe_module = Extension(
    "pysib._c._pysib_oe_core",
    sources=[
        "src/pysib/_c/sib_oe_module.c",
        "src/pysib/_c/sib_basic.c",
        "src/pysib/_c/sib_optimize.c",
    ],
    include_dirs=["src/pysib/_c", numpy.get_include()],
    libraries=lapack_libs,
    extra_link_args=lapack_link,
)

armax_module = Extension(
    "pysib._c._pysib_armax_core",
    sources=[
        "src/pysib/_c/sib_armax_module.c",
        "src/pysib/_c/sib_basic.c",
        "src/pysib/_c/sib_optimize.c",
    ],
    include_dirs=["src/pysib/_c", numpy.get_include()],
    libraries=lapack_libs,
    extra_link_args=lapack_link,
)

bj_module = Extension(
    "pysib._c._pysib_bj_core",
    sources=[
        "src/pysib/_c/sib_bj_module.c",
        "src/pysib/_c/sib_basic.c",
        "src/pysib/_c/sib_optimize.c",
    ],
    include_dirs=["src/pysib/_c", numpy.get_include()],
    libraries=lapack_libs,
    extra_link_args=lapack_link,
)

setup(
    ext_modules=[oe_module, armax_module, bj_module],
    exclude_package_data={"pysib._c": ["*.c", "*.h"]},
)
