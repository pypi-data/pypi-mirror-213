import os
import subprocess
import sys
from pathlib import Path

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import Extension, setup

PACKAGE_PATH = str(Path("edspdf_poppler").absolute())
POPPLER_PATH = str(Path("edspdf_poppler/poppler_src").absolute())

extra_compile_args = [
    "-std=c++17",
]

cmake_flags = [
    "-DBUILD_GTK_TESTS=OFF",
    "-DENABLE_BOOST=OFF",
    "-DENABLE_DCTDECODER=unmaintained",
    "-DENABLE_GLIB=OFF",
    "-DENABLE_GOBJECT_INTROSPECTION=OFF",
    "-DENABLE_LIBOPENJPEG=none",
    "-DENABLE_QT5=OFF",
    "-DENABLE_QT6=OFF",
    "-DENABLE_UTILS=OFF",
    "-DWITH_Cairo=OFF",
    "-DWITH_JPEG=OFF",
]

if sys.platform == "darwin":
    pass
if subprocess.run(["cmake", *cmake_flags, "."], cwd=POPPLER_PATH).returncode != 0:
    raise Exception("Poppler's cmake appear to have failed")
if subprocess.run(["make", "poppler"], cwd=POPPLER_PATH).returncode != 0:
    raise Exception("Poppler's make appear to have failed")

if sys.platform == "darwin":
    # OS X extras
    extra_compile_args.extend(
        [
            "-stdlib=libc++",  # "-mmacosx-version-min=10.7",
        ]
    )
    # See: https://stackoverflow.com/questions/53428219/cmake-rpath-origin-and-loader-path  # noqa: E501
    extra_link_args = [
        #    "-Wl,-rpath,@loader_path/poppler_src",
    ]
elif "linux" in sys.platform:
    # See: https://stackoverflow.com/questions/53428219/cmake-rpath-origin-and-loader-path  # noqa: E501
    extra_link_args = [
        #    "-Wl,-rpath,$ORIGIN/poppler_src",
    ]

poppler_ext = Extension(
    "edspdf_poppler.bindings",
    ["edspdf_poppler/bindings.pyx"],
    language="c++",
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    runtime_library_dirs=[POPPLER_PATH, PACKAGE_PATH],
    include_dirs=[POPPLER_PATH, os.path.join(POPPLER_PATH, "poppler")],
    library_dirs=[
        POPPLER_PATH,
    ],
    libraries=["poppler"],
)

setup(
    ext_modules=cythonize([poppler_ext]),
    package_data={
        "": ["*.dylib", "*.so"],
    },
    cmdclass={"build_ext": build_ext},
)
