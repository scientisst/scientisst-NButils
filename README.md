# ScientISST-NButils
scientisstNButils is a package for management of the ScientISST Notebooks repository. 


## Installation
Installation can be easily done with pip:

```bash
$ python3 -m pip install git+https://github.com/scientisst/scientisst-NButils.git
```

## Simple example

The code below should be run after all changes have been made to the local copy of the ScientISST Notebooks and before commiting changes and making a pull request to the original repository.

```bash
$ python3 -m scientisstNButils.createIndexTables [path to local copy of the ScientISST Notebooks repository]
```

This should create (or update) the MasterTable.md on the root of the repository, as well as the README.md files in each Chapter, with the complete index of all existing notebooks. 
