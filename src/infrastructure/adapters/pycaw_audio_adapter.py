from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from ctypes import cast, POINTER
from src.domain.ports.audio_interface_port import AudioInterfacePort
from src.domain.entities import AudioDevice, VolumeSettings


def com_initialized(func):
    def wrapper(*args, **kwargs):
        CoInitialize()
        try:
            return func(*args, **kwargs)
        finally:
            CoUninitialize()

    return wrapper


class PycawAudioAdapter(AudioInterfacePort):
    @com_initialized
    def get_all_devices(self) -> list[AudioDevice]:
        devices = AudioUtilities.GetAllDevices()
        return [
            AudioDevice(
                id=str(dev.id),
                name=dev.FriendlyName,
                is_input=self._is_input_device(dev),
                pycaw_device=dev,  # Almacenamos el dispositivo pycaw original
            )
            for dev in devices
        ]

    @com_initialized
    def get_volume_settings(self, device: AudioDevice) -> VolumeSettings:
        volume_interface = self._get_volume_interface(device)
        return VolumeSettings(
            volume=volume_interface.GetMasterVolumeLevelScalar(),
            is_muted=volume_interface.GetMute(),
        )

    @com_initialized
    def set_volume(self, device: AudioDevice, volume: float) -> None:
        volume_interface = self._get_volume_interface(device)
        volume_interface.SetMasterVolumeLevelScalar(volume, None)

    @com_initialized
    def set_mute(self, device: AudioDevice, is_muted: bool) -> None:
        volume_interface = self._get_volume_interface(device)
        volume_interface.SetMute(is_muted, None)

    def _get_volume_interface(self, device: AudioDevice):
        pycaw_device = self._get_or_recover_pycaw_device(device)
        if pycaw_device is None:
            raise ValueError(f"No se pudo encontrar el dispositivo: {device.name}")
        return pycaw_device.EndpointVolume

    def _get_or_recover_pycaw_device(self, device: AudioDevice):
        if hasattr(device, "pycaw_device") and device.pycaw_device is not None:
            return device.pycaw_device
        # Si no tenemos el pycaw_device, intentamos recuperarlo
        devices = AudioUtilities.GetAllDevices()
        return next((d for d in devices if str(d.id) == device.id), None)

    @com_initialized
    def _is_input_device(self, device):
        return AudioUtilities.GetEndpointDataFlow(device.id, outputType=1) == 1
