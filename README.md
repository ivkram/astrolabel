[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

Astrolabel is a lightweight Python package that allows to efficiently manage astronomy plot labels.

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
al.get_label('sfr')  # Output: '$\\mathrm{SFR}$ [$\\mathrm{M_{\\odot}\\,yr^{-1}}$]'
```

## Label Library

### Overview

Astrolabel reads the label data from a [YAML](https://yaml.org) file, which we call a _label library_. Here is an example of a minimal label library which contains only one label:

```yaml
formats:
  default: '_symbol_'
  default_u: '_symbol_ [_unit_]'

labels:
  sfr:
    symbol: '\mathrm{SFR}'
    unit: 'Msun / yr'                   # optional
    description: 'Star-formation rate'  # optional
```

The `formats` sections contains the list of template strings used by the `get_label()` method to format the label. When this method is called, `_symbol_` in the template string is replaced with the `symbol` attribute of the label, and `_unit_` is replaced with the `unit` attribute of the label.  Note that all template strings must come in two variants: one for labels with a unit, and another one for labels without a unit. The name of the template string where units are used must end with `_u` (e.g., `my_format_u`).

Here is a more advanced example of template strings which can be used to create labels with logarithms:
```yaml
  log: '$\log_{10}\,_symbol_$'
  log_u: '$\log_{10}\,_symbol_ / _unit_$'
```

To apply a custom label format to the label, specify the `fmt` argument of `get_label()`:

```python
al.get_label('sfr', fmt='log')  # Output: '$\\log_{10}\\,(\\mathrm{SFR} / (\\mathrm{M_{\\odot}\\,yr^{-1}}))$'
```

Next, the `labels` section contains the list of plot labels, each of which has the following attributes:

- `symbol`: the symbol representing the plotted parameter. Note that math mode is applied to all symbols by default. Therefore, use `\mathrm{}` in cases where the upright letter notation is preferable (e.g., `\mathrm{SFR}`);
- **\[optional\]** `unit`: the plotted parameter's unit of measurement. All units are converted to the LaTeX format using the Astropy's [`Quantity.to_string()`](https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity.to_string) method. The list of units supported by Astropy and thus by Astrolabel can be found in Astropy's official documentation [here](https://docs.astropy.org/en/stable/units/index.html). This list covers most (if not all) units used in astronomy. However, if you want to define new units, follow the instructions on [this page](https://docs.astropy.org/en/stable/units/combining_and_defining.html#defining-units);
- **\[optional\]** `description`: the text description of the plotted parameter.

**Note:** due to the specifics of YAML, it is highly recommended to use single quotes (`'`) when adding new labels or custom label formats to the label library.

### Loading a library from a file

```python
al = AstroLabels.read("---the full path to the label library goes here---")
```

### The default library

The location of the default label library is stored in the `DEFAULT_LIBRARY_PATH` constant:

```python
from astrolabel import DEFAULT_LIBRARY_PATH
print(DEFAULT_LIBRARY_PATH)  # Output: '/home/foo/.../astrolabel/astrolabel/data/astrolabel.yml'
```