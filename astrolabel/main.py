import astropy.units as u
import dacite
import yaml

from dataclasses import dataclass
import os
import pathlib
import sys
from typing import Union, Dict

__all__ = [
    "AstroLabel",
    "LabelLibrary"
]

DEFAULT_LIBRARY_PATH = pathlib.Path(__file__).parent / "data" / "astrolabel.yml"


@dataclass
class AstroLabel:
    symbol: str
    unit: Union[str, None] = None
    description: Union[str, None] = None


@dataclass
class LabelLibrary:
    formats: Dict[str, str]
    labels: Dict[str, AstroLabel]

    def __post_init__(self):
        self._library_path: pathlib.Path | None = None

    def library_fname(self):
        return self._library_path

    def info(self, output=None):
        if output is None:
            output = sys.stdout

        library_summary = []
        max_key_len = max(map(len, self.labels.keys()))
        for label_key, label_data in self.labels.items():
            library_summary.append(f"{label_key:>{max_key_len}}: {label_data.description}")

        output.write("\n".join(library_summary))
        output.write("\n")
        output.flush()

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
        if library_path.is_dir():
            raise IsADirectoryError(f"'{library_path}' is a directory")
        if not library_path.is_file():
            raise FileNotFoundError(f"File '{library_path}' does not exist")

        with open(library_path, "r") as label_library:
            label_data = yaml.safe_load(label_library)

        # create the LabelLibrary object
        ll = dacite.from_dict(data_class=cls, data=label_data, config=dacite.Config(strict=True))

        # store the path to the label library
        ll._library_path = library_path

        return ll

    @staticmethod
    def _substitute(template, key, value):
        i = template.index(key)
        if template[:i].count("$") % 2 == 1:
            value = value[1:-1]  # strip dollar signs
        return template.replace(key, value)

    def get_label(self, name: str, fmt: str = "default"):
        if name not in self.labels.keys():
            raise KeyError(f"Label key '{name}' does not exist")

        symbol = f"${self.labels[name].symbol}$"  # treat the symbol as math text
        unit = self.labels[name].unit

        label = self.formats[fmt + "_u"] if unit else self.formats[fmt]
        label = self._substitute(label, "__symbol__", symbol)

        if unit:
            unit_formatted = u.Unit(unit).to_string("latex_inline")
            label = self._substitute(label, "__unit__", unit_formatted)

        return label
