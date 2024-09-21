from abc import ABC, abstractmethod
from typing import Any


class SettingsPort(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def sync(self) -> None:
        pass
