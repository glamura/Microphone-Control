from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AudioDevice:
    id: str
    name: str
    is_input: bool
    pycaw_device: Optional[Any] = None


@dataclass
class VolumeSettings:
    volume: float
    is_muted: bool
