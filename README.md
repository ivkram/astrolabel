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

Create a `LabelLibrary` object:

```python
>>> from astrolabel import LabelLibrary
>>> ll = LabelLibrary.read()
```

Get a label by its key:

```python
>>> ll.get_label('sfr')  # output: '$\\mathrm{SFR}$ [$\\mathrm{M_{\\odot}\\,yr^{-1}}$]'
```

Change the label format:
```python
>>> ll.get_label('sfr', fmt='log')  # output: '$\\log_{10}\\,\\left(\\mathrm{SFR} / \\mathrm{M_{\\odot}\\,yr^{-1}}\\right)$'
```

Print the list of available labels:

```python
>>> ll.info()  # prints the list of available labels to the console
```

## Label Library

### Overview

Astrolabel reads the label data from a [YAML](https://yaml.org) file, which we call a _label library_. Here is an example of a minimal label library which contains only one label:

```yaml
formats:
  default: '__symbol__'
  default_u: '__symbol__ [__unit__]'

labels:
  sfr:
    symbol: '\mathrm{SFR}'
    unit: 'Msun yr-1'                   # optional
    description: 'Star-formation rate'  # optional
```

The `formats` sections contains the list of custom template strings used by the `get_label()` method to format the label. When this method is called, the template string is modified as follows: `__symbol__` is replaced with the `symbol` attribute of the label, and `__unit__` is replaced with the `unit` attribute of the label.  Note that all template strings must come in two variants: one for labels with a unit, and another one for labels without a unit. The name of the template string where units are used must end with `_u` (e.g., `my_format_u`).

Here is a more advanced example of template strings which can be used to create labels for plots with logarithmic axes:
```yaml
log: '$\log_{10}\,__symbol__$'
log_u: '$\log_{10}\,\left(__symbol__ / __unit__\right)$'
```

The `labels` section of the label library contains the list of custom plot labels, each of which has the following attributes:

- `symbol`: the symbol representing the plotted parameter. Note that math mode is applied to all symbols by default. Therefore, use `\mathrm{}` in cases where the upright letter notation is preferable (e.g., `\mathrm{SFR}`);
- **\[optional\]** `unit`: the plotted parameter's unit of measurement. All units are converted to the LaTeX format using the Astropy's [`Quantity.to_string()` method](https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity.to_string). The list of units supported by Astropy and hence by Astrolabel can be found in the Astropy's official documentation [here](https://docs.astropy.org/en/stable/units/index.html). This list covers most (if not all) units used in astronomy. However, if you want to define new units, follow the instructions on [this page](https://docs.astropy.org/en/stable/units/combining_and_defining.html#defining-units);
- **\[optional\]** `description`: the text description of the plotted parameter.

**Note:** due to the specifics of YAML, it is highly recommended to use single quotes (`'`) when adding new labels or label formats to the label library.

### Specifying the library location

The path to the label library can be passed to the `LabelLibrary` constructor:

```python
>>> ll = LabelLibrary.read('/path/to/label/library.yml')
```

In case no arguments are passed to the constructor, Astrolabel looks for the label library in three locations, in the following order:

1. `astrolabel.yml` in the current working directory.
2. `$ASTROLABEL` - the best option for users who want to use the same library across different projects.
3. The default library location (see below). Note that the default library will be overwritten each time you reinstall or update the package. 

To check the location of the currently active library, call the `library_fname()` method of the `LabelLibrary` object:

```python
>>> ll.library_fname()  # output: PosixPath('/home/foo/.../bar/astrolabel.yml')
```


### The default library

The Astrolabel package comes with a label library which includes two label formats (`default` and `log`) and some labels commonly used for astronomy plots. The location of the default label library is stored in the `DEFAULT_LIBRARY_PATH` constant:

```python
>>> from astrolabel import DEFAULT_LIBRARY_PATH
>>> DEFAULT_LIBRARY_PATH  # output: '/home/foo/.../astrolabel/astrolabel/data/astrolabel.yml'
```
