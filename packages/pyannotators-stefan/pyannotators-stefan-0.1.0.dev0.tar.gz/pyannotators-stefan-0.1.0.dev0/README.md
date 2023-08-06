# pyannotators_stefan

[![license](https://img.shields.io/github/license/oterrier/pyannotators_stefan)](https://github.com/oterrier/pyannotators_stefan/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_stefan/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_stefan/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_stefan)](https://codecov.io/gh/oterrier/pyannotators_stefan)
[![docs](https://img.shields.io/readthedocs/pyannotators_stefan)](https://pyannotators_stefan.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_stefan)](https://pypi.org/project/pyannotators_stefan/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_stefan)](https://pypi.org/project/pyannotators_stefan/)

My new Stefan Annotator

## Installation

You can simply `pip install pyannotators_stefan`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_stefan
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
