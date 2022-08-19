from setuptools import setup

VERSION = "0.0.1"
DESCRIPTION = "ScientISST-NButils is a package for management of the ScientISST Notebooks repository."

setup(
    name="scientisst-NButils",
    version=VERSION,
    description=DESCRIPTION,
    url="https://github.com/scientisst/scientisst-NButils.git",
    author="ScientISST",
    author_email="developer@scientisst.com",
    license="MIT",
    packages=["scientisst-NButils"],
    zip_safe=False,
)
