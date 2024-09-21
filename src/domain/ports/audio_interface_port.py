from abc import ABC, abstractmethod
from ..entities import AudioDevice, VolumeSettings


class AudioInterfacePort(ABC):
    @abstractmethod
    def get_all_devices(self) -> list[AudioDevice]:
        pass

    @abstractmethod
    def get_volume_settings(self, device: AudioDevice) -> VolumeSettings:
        pass

    @abstractmethod
    def set_volume(self, device: AudioDevice, volume: float) -> None:
        pass

    @abstractmethod
    def set_mute(self, device: AudioDevice, is_muted: bool) -> None:
        pass
