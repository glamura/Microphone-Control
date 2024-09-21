from dataclasses import dataclass


@dataclass(frozen=True)
class VolumeStep:
    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 1:
            raise ValueError("Volume step must be between 0 and 1")
