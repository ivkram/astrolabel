import astropy.units as u
import dacite
import yaml

from dataclasses import dataclass
import os
import pathlib
import re
import sys
from typing import Dict, List, Optional, Union, Tuple

__all__ = [
    "AstroLabel",
    "LabelLibrary"
]

DEFAULT_LIBRARY_PATH = pathlib.Path(__file__).parent / "data" / "astrolabel.yml"


@dataclass
class AstroLabel:
    symbol: str
    unit: Optional[str] = None
    description: Optional[str] = None
    wrap: bool = False


@dataclass
class LabelLibrary:
    formats: Dict[str, str]
    scripts: Optional[Dict[str, str]]
    labels: Dict[str, AstroLabel]

    def __post_init__(self):
        self._library_path: Optional[pathlib.Path] = None

    @property
    def library_path(self) -> Optional[pathlib.Path]:
        return self._library_path

    @property
    def _fmt_names(self) -> List[str]:
        return [key for key in self.formats.keys() if not key.endswith('_u')]

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
    def read(cls, filename: Optional[Union[str, pathlib.Path]] = None):
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
    def _substitute(template: str, key: str, value: str) -> str:
        i = template.index(key)
        if template[:i].count("$") % 2 == 1:
            value = value[1:-1]  # strip dollar signs
        return template.replace(key, value)

    def _parse_name(self, name) -> Tuple[AstroLabel, List[str], List[str]]:
        subs = re.findall(r'_([a-zA-Z0-9]+)', name)
        sups = re.findall(r'\^([a-zA-Z0-9]+)', name)

        name = name.split('_')[0].split('^')[0]

        if name not in self.labels.keys():
            raise KeyError(f"Label key '{name}' not found")
        for sub in subs:
            if sub not in self.scripts.keys():
                raise KeyError(f"Subscript '{sub}' not found")
        for sup in subs:
            if sup not in self.scripts.keys():
                raise KeyError(f"Superscript '{sup}' not found")

        subs = [self.scripts[sub] for sub in subs if self.scripts[sub]]
        sups = [self.scripts[sup] for sup in sups if self.scripts[sup]]

        return self.labels[name], subs, sups


    @staticmethod
    def _format_symbol(symbol: str, subs: Optional[List[str]] = None, sups: Optional[List[str]] = None, wrap: bool = False) -> str:
        if wrap:
            symbol = fr"\left({symbol}\right)"
        if subs:
            symbol += "_{"
            symbol += ",".join(subs)
            symbol += "}"
        if sups:
            symbol += "^{"
            symbol += ",".join(sups)
            symbol += "}"
        symbol = f"${symbol}$"  # treat symbols as math text
        return symbol

    @staticmethod
    def _format_unit(unit: str, scale: float = None) -> str:
        unit = u.Unit(unit)
        if scale:
            unit = u.Unit(scale * unit)

        unit = unit.to_string("latex_inline")
        if unit.startswith(r"$\mathrm{1 \times "):
            unit = unit.replace(r"1 \times ", r"")

        return unit

    def get_label(self, name: str, fmt: str = 'linear', scale: float = None):
        al, subs, sups = self._parse_name(name)

        if fmt not in self.formats.keys():
            raise ValueError(f"Label format '{fmt}' not found. Available formats: {', '.join(self._fmt_names)}")
        if al.unit:
            fmt += "_u"

        label = self.formats[fmt]

        symbol_formatted = self._format_symbol(al.symbol, subs=subs, sups=sups, wrap=al.wrap)
        label = self._substitute(label, "__symbol__", symbol_formatted)

        if al.unit:
            unit_formatted = self._format_unit(al.unit, scale)
            label = self._substitute(label, "__unit__", unit_formatted)

        return label

    def get_symbol(self, name: str):
        al, subs, sups = self._parse_name(name)
        symbol_formatted = self._format_symbol(al.symbol, subs=subs, sups=sups)

        return symbol_formatted
