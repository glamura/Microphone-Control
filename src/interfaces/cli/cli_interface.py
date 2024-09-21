from ...application.services.audio_control_service import AudioControlService
from ...application.services.settings_service import SettingsService


class CLI:
    def __init__(
        self, audio_service: AudioControlService, settings_service: SettingsService
    ):
        self.audio_service = audio_service
        self.settings_service = settings_service

    def run(self):
        print("Microphone Control CLI")
        while True:
            command = input("Enter command (list, up, down, mute, exit): ").lower()
            if command == "exit":
                break
            elif command == "list":
                self.list_devices()
            elif command in ["up", "down"]:
                self.change_volume(command)
            elif command == "mute":
                self.toggle_mute()
            else:
                print("Invalid command")

    def list_devices(self):
        devices = self.audio_service.get_input_devices()
        for device in devices:
            print(f"ID: {device.id}, Name: {device.name}")

    def change_volume(self, direction):
        device_id = input("Enter device ID: ")
        step = float(input("Enter volume step (0-1): "))
        device = self.audio_service.get_device_by_id(device_id)
        if device:
            if direction == "up":
                new_volume = self.audio_service.volume_up(device, step)
            else:
                new_volume = self.audio_service.volume_down(device, step)
            print(f"New volume: {new_volume:.2f}")
        else:
            print("Device not found")

    def toggle_mute(self):
        device_id = input("Enter device ID: ")
        device = self.audio_service.get_device_by_id(device_id)
        if device:
            is_muted = self.audio_service.toggle_mute(device)
            print(f"Microphone {'muted' if is_muted else 'unmuted'}")
        else:
            print("Device not found")
