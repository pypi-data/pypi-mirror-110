# pysegmenters_spacyrules

[![license](https://img.shields.io/github/license/oterrier/pysegmenters_spacyrules)](https://github.com/oterrier/pysegmenters_spacyrules/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pysegmenters_spacyrules/workflows/tests/badge.svg)](https://github.com/oterrier/pysegmenters_spacyrules/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pysegmenters_spacyrules)](https://codecov.io/gh/oterrier/pysegmenters_spacyrules)
[![docs](https://img.shields.io/readthedocs/pysegmenters_spacyrules)](https://pysegmenters_spacyrules.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pysegmenters_spacyrules)](https://pypi.org/project/pysegmenters_spacyrules/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysegmenters_spacyrules)](https://pypi.org/project/pysegmenters_spacyrules/)

Rule based segmenter based on Spacy

## Installation

You can simply `pip install pysegmenters_spacyrules`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pysegmenters_spacyrules
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
