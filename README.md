[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

Astrolabel is a lightweight Python package that allows to efficiently manage labels of astronomy plots.

## Installation

```shell
$ pip install astrolabel
```

## Requirements

- `python>=3.8`
- `astropy>=5.0`
- `dacite>=1.8.0`

## Quick Start

Create an `AstroLabels` object:

```python
from astrolabel import AstroLabels
al = AstroLabels.read()
```

Get a label by its key:

```python
al.get_label('sfr')
```

Output:
```python
'$\\mathrm{SFR}$ [$\\mathrm{M_{\\odot}\\,yr^{-1}}$]'
```