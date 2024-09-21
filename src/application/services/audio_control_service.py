from src.domain.ports.audio_interface_port import AudioInterfacePort
from src.domain.entities import AudioDevice


class AudioControlService:
    def __init__(self, audio_interface: AudioInterfacePort):
        self.audio_interface = audio_interface

    def volume_up(self, device: AudioDevice, step: float) -> tuple[float, bool]:
        current_settings = self.audio_interface.get_volume_settings(device)
        new_volume = min(1.0, self._round_to_step(current_settings.volume + step, step))
        self.audio_interface.set_volume(device, new_volume)
        return new_volume, current_settings.is_muted

    def volume_down(self, device: AudioDevice, step: float) -> tuple[float, bool]:
        current_settings = self.audio_interface.get_volume_settings(device)
        new_volume = max(0.0, self._round_to_step(current_settings.volume - step, step))
        self.audio_interface.set_volume(device, new_volume)
        return new_volume, current_settings.is_muted

    def toggle_mute(self, device: AudioDevice) -> bool:
        current_settings = self.audio_interface.get_volume_settings(device)
        new_mute_state = not current_settings.is_muted
        self.audio_interface.set_mute(device, new_mute_state)
        return new_mute_state

    def _round_to_step(self, value: float, step: float) -> float:
        return round(value / step) * step

    def get_input_devices(self) -> list[AudioDevice]:
        return [
            device
            for device in self.audio_interface.get_all_devices()
            if device.is_input
        ]
