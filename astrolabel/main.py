import astropy.units as u
import dacite
import yaml

from dataclasses import dataclass
import os
import pathlib
from typing import Union, Dict


DEFAULT_LIBRARY_PATH = pathlib.Path(__file__).parent / 'data' / 'astrolabel.yml'


@dataclass
class Label:
    symbol: str
    unit: Union[str, None]
    description: Union[str, None]


@dataclass
class AstroLabels:
    formats: Dict[str, str]
    labels: Dict[str, Label]

    def __post_init__(self):
        self._library_path: pathlib.Path | None = None

    def library_fname(self):
        return self._library_path

    @staticmethod
    def _get_library_path() -> pathlib.Path:
        # search for a library in the working directory
        library_path = pathlib.Path() / "astrolabel.yml"
        if library_path.exists():
            return library_path

        # use the path stored in the environment variable - if not set, use the path to the default library
        library_path = os.environ.get("ASTROLABEL", default=DEFAULT_LIBRARY_PATH)
        return pathlib.Path(library_path)

    @classmethod
    def read(cls, filename: Union[str, pathlib.Path, None] = None):
        if filename is None:
            library_path = cls._get_library_path()
        else:
            library_path = pathlib.Path(filename)

        library_path = library_path.resolve()
        if not library_path.is_file():
            raise FileNotFoundError(f"The file \"{library_path}\" does not exist")

        with open(library_path, "r") as label_library:
            label_data = yaml.safe_load(label_library)

        # create the AstroLabels object
        al = dacite.from_dict(data_class=cls, data=label_data, config=dacite.Config(strict=True))

        # store the path to the label library
        al._library_path = library_path

        return al

    @staticmethod
    def _replace(label, key, value):
        i = label.index(key)
        if label[:i].count('$') % 2 == 1:
            value = value[1:-1]  # strip dollar signs
        return label.replace(key, value)

    def get_label(self, name: str, fmt: str = 'default'):
        symbol = f'${self.labels[name].symbol}$'  # treat the symbol as math text
        unit_plain = self.labels[name].unit

        label = self.formats[fmt + '_u'] if unit_plain else self.formats[fmt]
        label = self._replace(label, '_symbol_', symbol)

        if unit_plain:
            unit = u.Unit(unit_plain).to_string('latex_inline')
            label = self._replace(label, '_unit_', unit)

        return label
