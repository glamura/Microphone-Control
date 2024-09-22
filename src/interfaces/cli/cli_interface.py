import sys
import platform

if platform.system() != "Windows":
    from src.infrastructure.hotkey_handler import hotkey_handler


class CLIInterface:
    def __init__(self, audio_service):
        self.audio_service = audio_service
        self.current_device = None
        self.volume_step = 5
        self.default_hotkeys = {
            "volume_up": "ctrl+shift+u",
            "volume_down": "ctrl+shift+d",
            "mute_toggle": "ctrl+shift+m",
        }

    def run(self):
        print("Control de Micrófono - Interfaz de Línea de Comandos")
        print("Sistema operativo detectado:", platform.system())

        self.select_device()
        self.set_volume_step()
        self.configure_hotkeys()

        print("\nAplicación ejecutándose en segundo plano. Presione Ctrl+C para salir.")
        try:
            hotkey_handler.start_listening()
            while True:
                pass  # Mantener la aplicación en ejecución
        except KeyboardInterrupt:
            print("\nDeteniendo la aplicación...")
            hotkey_handler.stop_listening()

    def select_device(self):
        devices = self.audio_service.get_input_devices()
        if not devices:
            print("No se encontraron dispositivos de entrada.")
            sys.exit(1)

        print("\nDispositivos de entrada disponibles:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device.name}")

        while True:
            try:
                choice = int(input("Seleccione el número del dispositivo: ")) - 1
                if 0 <= choice < len(devices):
                    self.current_device = devices[choice]
                    print(f"Dispositivo seleccionado: {self.current_device.name}")
                    break
                else:
                    print("Selección inválida. Intente de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def set_volume_step(self):
        while True:
            try:
                step = int(input("Ingrese el paso de volumen (1-20): "))
                if 1 <= step <= 20:
                    self.volume_step = step
                    print(f"Paso de volumen establecido a {step}")
                    break
                else:
                    print("El paso debe estar entre 1 y 20.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def configure_hotkeys(self):
        actions = {
            "volume_up": self.volume_up,
            "volume_down": self.volume_down,
            "mute_toggle": self.mute_toggle,
        }
        for action, callback in actions.items():
            while True:
                default_key = self.default_hotkeys[action]
                key = input(
                    f"Ingrese la tecla para {action} (por defecto '{default_key}'): "
                )
                if not key:
                    key = default_key
                if self.is_valid_hotkey(key):
                    hotkey_handler.add_hotkey(key, callback)
                    print(f"Atajo configurado para {action}: {key}")
                    break
                else:
                    print(
                        "Combinación de teclas no válida. Por favor, intente de nuevo."
                    )

    def is_valid_hotkey(self, hotkey):
        valid_modifiers = {"ctrl", "shift", "alt"}
        parts = hotkey.lower().split("+")
        if len(parts) < 2:
            return False
        modifiers = set(parts[:-1])
        key = parts[-1]
        return modifiers.issubset(valid_modifiers) and len(key) == 1 and key.isalnum()

    def volume_up(self):
        if self.current_device:
            new_volume, _ = self.audio_service.volume_up(
                self.current_device, self.volume_step / 100
            )
            print(f"Volumen subido a {int(new_volume * 100)}%")

    def volume_down(self):
        if self.current_device:
            new_volume, _ = self.audio_service.volume_down(
                self.current_device, self.volume_step / 100
            )
            print(f"Volumen bajado a {int(new_volume * 100)}%")

    def mute_toggle(self):
        if self.current_device:
            is_muted = self.audio_service.toggle_mute(self.current_device)
            print(f"Micrófono {'silenciado' if is_muted else 'activado'}")
