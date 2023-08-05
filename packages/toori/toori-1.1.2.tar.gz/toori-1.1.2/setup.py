
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pathlib

__version__ = "1.1.2"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        "_toori",
        ["toori/main.cpp"],
        # Example: passing in the version to the compiled code
        # define_macros=[("VERSION_INFO", __version__)],
        include_dirs=["external/WinDivert-2.2.2-A/include"],
        library_dirs=["external/WinDivert-2.2.2-A/x64"],
        libraries=["WinDivert"],  # WinDivert.lib
    ),
]

setup(
    name="toori",
    version=__version__,
    url="https://github.com/kokseen1/toori",
    description="A minimal layer 3 tunnel over http(s).",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    # extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
    data_files=[
        (
            "",
            [
                "external/WinDivert-2.2.2-A/include/windivert.h",
                "external/WinDivert-2.2.2-A/x64/WinDivert.dll",
                "external/WinDivert-2.2.2-A/x64/WinDivert64.sys",
                "external/WinDivert-2.2.2-A/x64/WinDivert.lib",
            ],
        )
    ],
    include_package_data=True,
    packages=["toori"],
    package_dir={
        "toori": "toori",
    },
    entry_points={
        "console_scripts": [
            "toori = toori.console:main",
        ]
    },
    install_requires=[
        "python-socketio",
        "aiohttp",
    ],
)
