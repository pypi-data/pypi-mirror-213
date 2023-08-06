# voila-material-tuwien

Material design template for voila

## Installation

You can install it using pip:

```
pip install voila-material-tuwien
```

Or using conda:

```
conda install -c conda-forge voila-material-tuwien
```

## Development Installation

To see your active changes install the template via: 

```
pip install -e .
```

## Usage

```
voila my_notebook.ipynb --template=material-tuwien
```

Or for the dark theme:

```
voila my_notebook.ipynb --template=material-tuwien --theme=dark
```

## Release

Deletes last locally built version.

```
rm -rf dist/*
```

Build package:

```
python -m build
```

Upload to PyPi:
```
twine upload dist/*
```
