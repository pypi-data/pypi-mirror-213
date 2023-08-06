from typing import Any

from attrs import define

from nutorious.config import Config
from nutorious.model import Journal


@define
class Context:
    config: Config
    journal: Journal
    options: Any
