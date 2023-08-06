from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import cattrs
import yaml
from attrs import define, field

from nutorious.utils.collections import merge_dicts
from nutorious.utils.commons import load_yaml_data


@define
class Config:
    meals: list[str]
    ui: UiConfig


@define
class UiConfig:
    daily: DailyConfig
    # diff: DiffConfig


@define
class DailyConfig:
    title: str
    columns: list[ColumnConfig]


@define
class ColumnConfig:
    data: str
    title: str = field()
    style: str = "white"
    justify: str = "right"

    @title.default
    def __default_title(self):
        return self.data


# @define
# class DiffConfig:
#     columns: list[str]


def load_config(journal_path: str) -> Config:
    default_config_text = (files("nutorious.config") / "default.yml").read_text("UTF-8")
    config_data = yaml.safe_load(default_config_text)

    journal_config_path = Path(journal_path) / "config.yml"
    if journal_config_path.exists():
        journal_config_data = load_yaml_data(journal_config_path)
        config_data = merge_dicts(config_data, journal_config_data)

    config = cattrs.structure(config_data, Config)
    return config
