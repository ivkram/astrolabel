import astropy.units as u
import dacite
import yaml

from dataclasses import dataclass
import pathlib
from typing import Union, Dict


@dataclass
class Label:
    symbol: str
    unit: Union[str, None]
    description: Union[str, None]


@dataclass
class AstroLabels:
    formats: Dict[str, str]
    labels: Dict[str, Label]

    @classmethod
    def read(cls, filename: Union[str, None] = None):
        if filename is None:
            filename = pathlib.Path(__file__).parent / 'data' / 'astrolabel.yml'

        with open(filename, "r") as yaml_file:
            label_data = yaml.safe_load(yaml_file)

        return dacite.from_dict(data_class=cls, data=label_data, config=dacite.Config(strict=True))

    @staticmethod
    def replace(label, key, value):
        i = label.index(key)
        if label[:i].count('$') % 2 == 1:
            value = value[1:-1]  # strip dollar signs
        return label.replace(key, value)

    def get_label(self, name: str, fmt: str = 'default'):
        symbol = f'${self.labels[name].symbol}$'  # treat the symbol as math text
        unit_plain = self.labels[name].unit

        label = self.formats[fmt + '_u'] if unit_plain else self.formats[fmt]
        label = self.replace(label, '_symbol_', symbol)

        if unit_plain:
            unit = u.Unit(unit_plain).to_string('latex_inline')
            label = self.replace(label, '_unit_', unit)

        return label
