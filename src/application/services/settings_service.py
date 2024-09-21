from ...domain.ports.settings_port import SettingsPort


class SettingsService:
    def __init__(self, settings_port: SettingsPort):
        self.settings_port = settings_port

    def get_setting(self, key: str, default: any = None) -> any:
        return self.settings_port.get(key, default)

    def set_setting(self, key: str, value: any) -> None:
        self.settings_port.set(key, value)
        self.settings_port.sync()

    def save_all_settings(self, settings: dict) -> None:
        for key, value in settings.items():
            self.settings_port.set(key, value)
        self.settings_port.sync()
