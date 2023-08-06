# Bospell
[![PyPI version](https://badge.fury.io/py/bospell.svg)](https://badge.fury.io/py/bospell)
[![Test](https://github.com/Esukhia/bospell/actions/workflows/test.yml/badge.svg)](https://github.com/Esukhia/bospell/actions/workflows/test.yml)
[![Test Coverage](https://github.com/Esukhia/bospell/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/Esukhia/bospell/actions/workflows/test-coverage.yml)
[![Publish](https://github.com/Esukhia/bospell/actions/workflows/deloy.yml/badge.svg)](https://github.com/Esukhia/bospell/actions/workflows/deloy.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Spell checking toolkit for Tibetan (Boyig)

## Installation
The easiest method to install is using pip:

```bash
pip install bospell
```

To install from source:
```bash
git clone https://github.com/Esukhia/bospell.git
cd bospell
python setup.py install
```

## Quickstart
After installation, using `bospell` should be fairly straight forward:
```python
>>> from bospell import Text
>>> text = Text("བོད་པའི་བུ་བཀྲ་ཤིད་")
>>> text.corrected
'བོད་པའི་བུ་བཀྲ་ཤིས'
>>> text.suggestions
{3: Suggestions(candidates=['བཀྲ་ཤིས', 'བཀྲ་ཤིས་པ', 'བཀྲ་ཤིས་མ'], span=Span(start=11, end=19))}
```

## Development
```bash
git clone https://github.com/Esukhia/bospell.git
cd bospell
pip install -r requirements.txt
pre-commit install
pip install -e .
```

## Testing
```
pytest tests
```
