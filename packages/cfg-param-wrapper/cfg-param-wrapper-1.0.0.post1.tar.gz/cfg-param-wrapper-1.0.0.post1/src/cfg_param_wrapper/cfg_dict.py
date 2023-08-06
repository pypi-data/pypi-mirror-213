"""A dictionary subclass used for fast dictionary json usage."""

import json
import os
from pathlib import Path
from typing import Any, Literal
from .save_handlers import HANDLERS, SaveHandler


class CfgDict(dict):
    """
    A subclass of `dict` with some useful changes, most notably
    storing a path to save, including saving methods
    """

    def __init__(
        self,
        cfg_path: str | Path,
        config: dict | None = None,
        autofill: bool = False,
        save_on_change: bool = False,
        sort_on_save: bool = False,
        start_empty: bool = False,
        save_mode: Literal["json", "toml"] = "json",
    ) -> None:
        config = config or {}
        super().__init__(config)
        self.cfg_path: str | Path = cfg_path
        self.save_on_change: bool = save_on_change
        self.sort_on_save: bool = sort_on_save

        assert save_mode in HANDLERS
        self.save_handler: SaveHandler = HANDLERS[save_mode](cfg_path)

        if not os.path.exists(self.cfg_path) and autofill:
            self.save(config)
        if not start_empty:
            self.load()

    def set_path(self, path):
        """sets a new path to follow"""
        self.cfg_path = path
        self.save_handler.path = path
        return self

    def save(self, out_dict=None):
        """saves the dict to the file"""
        if not isinstance(out_dict, dict):
            out_dict = self
        if self.sort_on_save:
            out_dict = dict(sorted(out_dict.items()))
        self.save_handler.save(dict(out_dict))
        return self

    def _save_on_change(self) -> bool:
        if self.save_on_change:
            self.save()
            return True
        return False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._save_on_change()
        return self

    def pop(self, *args, **kwargs):
        super().pop(*args, **kwargs)
        self._save_on_change()
        return self

    def clear(self):
        super().clear()
        return self

    def load(self):
        """Loads the data from the file"""
        if os.path.exists(self.cfg_path):
            try:
                self.update(self.save_handler.load())
            except Exception:
                print(f"[!] failed to load config from {self.cfg_path}")
        else:
            self.save({})
        return self

    @staticmethod
    def is_json_serializable(obj: Any) -> bool:
        """checks if an object is JSON Serializable"""
        try:
            json.dumps(obj)
            return True
        except (TypeError, OverflowError):
            return False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.save_on_change:
            self.save()

    def __delitem__(self, key):
        super().__delitem__(key)
        if self.save_on_change:
            self.save()
