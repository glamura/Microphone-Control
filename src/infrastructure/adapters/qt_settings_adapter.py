from PyQt5.QtCore import QSettings
from ...domain.ports.settings_port import SettingsPort


class QtSettingsAdapter(SettingsPort):
    def __init__(self, organization: str, application: str):
        self.settings = QSettings(organization, application)

    def get(self, key: str, default: any = None) -> any:
        return self.settings.value(key, default)

    def set(self, key: str, value: any) -> None:
        self.settings.setValue(key, value)

    def sync(self) -> None:
        self.settings.sync()
