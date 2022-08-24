# ScientISST-NButils
scientisstNButils is a package for management of the ScientISST Notebooks repository. 


## Installation
Installation can be easily done with pip:

```bash
python3 -m pip install git+https://github.com/scientisst/scientisst-NButils.git
```

## Simple example

The code below should be run after all changes have been made to the local copy of the ScientISST Notebooks and before commiting changes and making a pull request to the original repository.

```bash
python3 -m scientisstNButils.createIndexTables [path to local copy of the ScientISST Notebooks repository]
```

This should create (or update) the MasterTable.md on the root of the repository, as well as the README.md files in each Chapter, with the complete index of all existing notebooks. 

## Contribution Guide
This contribution guide provides some guidelines to add or update content to the [ScientISST Notebooks](https://github.com/scientisst/notebooks.git). Further information regarding the initial steps can be found in [this post](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/).

### Fork the ScientISST Notebooks repository to your account

### Make a local clone and add a remote

```bash
git remote add upstream https://github.com/scientisst/notebooks.git
```

### Create your own branch 
We suggest naming it with the same ID of the notebook (e.g. A001).

```bash
git checkout -b [branch name] 
```

### Make and commit changes
Create or update notebooks and resources at will. Then commit them and push your changes to the remote repository.

```bash
git add .
git commit -m "[your commit message]"
git push [remote] [branch name]
```

### Opening a Pull Request
> _GitHub makes this part incredibly easy. Once you push a new branch up to your repository, GitHub will prompt you to create a pull request (I’m assuming you’re using your browser and not the GitHub native apps)._

This will open a revision "issue" with the maintainers of the repository (us), where we'll discuss and approve the changes.

### Cleaning up
After merging your changes with the original repository, do as follows:

```bash
git checkout [main branch name] 
git pull upstream [main branch name] 
git branch -d [branch name]
git push origin [main branch name]
git push --delete origin [branch name]
```

### For later use
Whenever you want to make new changes to the original repository, don't forget to first sync your fork:

```bash
git pull upstream [main branch name]
git push origin [main branch name]
```

###### Glossary
**upstream**: original (remote) ScientISST Notebooks repository 

**origin**: your (remote) forked repository

**main**: name of the main branch (usually main or master)


