from ...domain.entities import AudioDevice
from ...domain.ports.audio_interface_port import AudioInterfacePort


class AudioDeviceRepository:
    def __init__(self, audio_interface: AudioInterfacePort):
        self.audio_interface = audio_interface

    def get_all_devices(self) -> list[AudioDevice]:
        return self.audio_interface.get_all_devices()

    def get_input_devices(self) -> list[AudioDevice]:
        return [device for device in self.get_all_devices() if device.is_input]

    def get_device_by_id(self, device_id: str) -> AudioDevice:
        devices = self.get_all_devices()
        return next((device for device in devices if device.id == device_id), None)
