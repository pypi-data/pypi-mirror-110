# manpy

`manpy` is a simple lightweight python tool to ease the creation of python package, with a support for conda packaging.


## Installation

To use install the package either by conda:
```bash
conda install -c fgacon manpy
```

or from source:
```bash
python -m pip install . -v
```

## Usage
Use the cli of the package:
```bash
manpy
```
It will create the following python package architecture in the current folder.

```
./
├──PGK_NAME/
|  └──__init__.py
├──conda/ (optionnal)
|  └──env.yaml/
└──setup.py
```
