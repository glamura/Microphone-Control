from dataclasses import dataclass
from typing import Any


@dataclass
class AudioDevice:
    id: str
    name: str
    is_input: bool
    pycaw_device: Any


@dataclass
class VolumeSettings:
    volume: float
    is_muted: bool
