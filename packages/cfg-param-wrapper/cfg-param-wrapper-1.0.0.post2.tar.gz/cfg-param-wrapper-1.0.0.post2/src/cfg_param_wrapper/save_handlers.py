from __future__ import annotations

import json
from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

import toml


class SaveHandler:
    def __init__(self, path: str | Path):
        self.path: Path = Path(path)

    @abstractmethod
    def save(self, dct: dict) -> None:
        """saves the given dict to self.path"""

    @abstractmethod
    def load(self) -> dict:
        """loads a dictionary from self.path"""

    @abstractmethod
    def try_serialize(self, object: object) -> bool:
        """Tries to serialize the item and returns whether it is successful"""

    def _write(self, func: Callable, mode="w") -> None:
        with open(self.path, mode, encoding="utf-8") as file:
            func(file)

    def _read(self, func: Callable, mode="r") -> Any:
        with open(self.path, mode, encoding="utf-8") as file:
            return func(file)


class JsonSaveHandler(SaveHandler):
    """A save handler made to save and load .json files"""

    def save(self, dct: dict) -> None:
        self._write(lambda file: json.dump(dct, file, indent=4))

    def load(self) -> dict:
        return self._read(json.load)

    def try_serialize(self, object: object) -> bool:
        try:
            json.dumps(object)
            return True
        except (TypeError, OverflowError):
            return False

class TomlSaveHandler(SaveHandler):
    """A save handler made to save and load .toml files"""

    def save(self, dct: dict) -> None:
        self._write(lambda file: toml.dump(dct, file))

    def load(self) -> dict:
        return self._read(toml.load)

    def try_serialize(self, object: object) -> bool:
        try:
            toml.dumps(object)
            return True
        except (TypeError, OverflowError, ValueError):
            return False

HANDLERS: dict[str, type[SaveHandler]] = {"json": JsonSaveHandler, "toml": TomlSaveHandler}
