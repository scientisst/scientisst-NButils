# ScientISST-NButils
scientisstNButils is a package for management of the ScientISST Notebooks repository. 

> ⚠️ **WARNING:** Currently, this package is only supported by Unix systems. If you are woking with a Windows OS, follow the **Contribution Guide** below and alert this fact to the reviewers!

## Installation
Installation can be easily done with pip:

```bash
python3 -m pip install git+https://github.com/scientisst/scientisst-NButils.git
```

## Contribution Guide
This contribution guide provides some guidelines to add or update content to the [ScientISST Notebooks](https://github.com/scientisst/notebooks.git). Further information regarding the initial steps can be found in [this post](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/).

### 1. Fork the ScientISST Notebooks repository to your account

This will only be done once - creating your own copy of the ScientISST Notebooks repository. 

### 2. Make a local clone and add a remote

```bash
git remote add upstream https://github.com/scientisst/notebooks.git
```

### 3. Create a branch
This is not mandatory, but it's good practice to create a branch for specific alterations you plan to make.
We suggest naming it with the same ID of the notebook (e.g. A001).

```bash
git checkout -b [branch name] 
```

### 4. Make and commit changes
Create or update notebooks and resources at will. Use the temaplate available [here](https://github.com/scientisst/notebooks/tree/master/_Templates/notebook_template) and don't forget to place all resources in the respective _\_Resources_ directory.

Don't forget to commit your changes and push them to the remote repository (this can be done anytime throughout your changes).

```bash
git add .
git commit -m "[your commit message]"
git push [remote] [branch name]
```

### 5. Use ScientISST-NButils

**The examples below should be run after all changes have been made to the local copy of the ScientISST Notebooks and before commiting changes and making a pull request to the original repository.**

- To create (or update) the MasterTable.md on the root of the repository, as well as the README.md files in each Chapter, with the complete index of all existing notebooks _(path -> path to local copy of the ScientISST Notebooks repository)_:
```bash
scientisst_index_tables -d [path]
```

- For Notebooks that have absolute paths to images, download images to respective _\_Resources_ directory and replace link:
```bash
scientisst_links_to_relative -d [path]
```

### 6. Opening a Pull Request
Once you have finished your changes, press `Contribute` on your Notebooks fork page (using the GitHub browser).

This will open a revision "issue" with the maintainers of the repository (us), where we'll discuss and approve the changes.

### 7. Cleaning up
After merging your changes with the original repository, do as follows:

```bash
git checkout [main branch name] 
git pull upstream [main branch name] 
git branch -d [branch name]
git push origin [main branch name]
git push --delete origin [branch name]
```

### 8. For later use
Whenever you want to make new changes to the original repository, don't forget to first sync your fork:

```bash
git pull upstream [main branch name]
git push origin [main branch name]
```

###### Glossary
**upstream**: original (remote) ScientISST Notebooks repository 

**origin**: your (remote) forked repository

**main**: name of the main branch (usually main or master)


