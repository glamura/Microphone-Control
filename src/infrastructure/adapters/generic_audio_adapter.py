from src.domain.ports.audio_interface_port import AudioInterfacePort
from src.domain.entities import AudioDevice, VolumeSettings


class GenericAudioAdapter(AudioInterfacePort):
    def __init__(self):
        self.dummy_device = AudioDevice(id="dummy", name="Dummy Device", is_input=True)
        self.volume = 0.5
        self.is_muted = False

    def get_all_devices(self) -> list[AudioDevice]:
        return [self.dummy_device]

    def get_volume_settings(self, device: AudioDevice) -> VolumeSettings:
        return VolumeSettings(volume=self.volume, is_muted=self.is_muted)

    def set_volume(self, device: AudioDevice, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))

    def set_mute(self, device: AudioDevice, is_muted: bool) -> None:
        self.is_muted = is_muted

    def _is_input_device(self, device):
        return True
