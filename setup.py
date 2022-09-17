from importlib.metadata import entry_points
from setuptools import setup

VERSION = "0.2.6"
DESCRIPTION = "ScientISST-NButils is a package for management of the ScientISST Notebooks repository."

setup(
    name="scientisstNButils",
    version=VERSION,
    description=DESCRIPTION,
    url="https://github.com/scientisst/scientisst-NButils.git",
    author="ScientISST",
    author_email="developer@scientisst.com",
    entry_points={
        "console_scripts": [
            "scientisst_links_to_relative=scientisstNButils.update_formating:links_to_relative_cli",
            "scientisst_index_tables=scientisstNButils.create_index_tables:create_index_tables_cli",
        ]
    },
    license="MIT",
    packages=["scientisstNButils"],
    zip_safe=False,
)
