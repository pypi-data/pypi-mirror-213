# Gamedev-pyved

A new Game Creation toolbox (+the associated visual editor) 100% based on Python.
**And it’s open-source**

## Installation for end users

```
pip get install pyved
```

## Getting started (the Dev mode)

```
git clone https://github.com/wkta/gamedev-pyved.git

# create a separate different folder, create a virtual environment!
cd ..
mkdir testing-pyved
cd testing-pyved
python -m venv venv

# activate the VENV, install pyved-engine in editable mode
venv\Scripts\activate.bat
# (move to the folder where one should the game engine)
cd ..\pyved-engine
pip install -e .

# go back to pyved and install basic requirements, then,
# also install it in editable mode
cd ..\gamedev-pyved
pip install -r requirements.txt
pip install -e .

```
Your are ready to use/mod the `pyved` toolbox, at last!
```
cd ..\testing-pyved
pyved new myProject
pyved open myProject\pyved.json
```


## Disclaimer

This is an *experimental technology* (proof-of-concept).
therefore it is still very raw and unfinished

If you wish to contruibute, be our guest! <3
You can create pull requests directly, or send an e-mail to thomas.iw@kata.games if you want to discuss with the project maintainer.


### (Recipe for the core team)

1. create a PYTHON package using `make_package.bat` (uses `setup.py`+the whole folder)
1. after extensive testing under virtual env, publish the release with: `twine upload dist/*`
