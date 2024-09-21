from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QPushButton,
    QGroupBox,
    QSystemTrayIcon,
    QMenu,
    QStyle,
    QAction,
    QApplication,
)
from PyQt5.QtCore import QSettings, QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from src.interfaces.gui.widgets.key_sequence_edit import KeySequenceEdit
from src.interfaces.gui.widgets.volume_tooltip import VolumeTooltip
from src.interfaces.gui.widgets.alert_widget import AlertWidget
from src.application.services.audio_control_service import AudioControlService
from src.domain.entities import AudioDevice
import keyboard


class MicrophoneControlGUI(QMainWindow):
    update_tooltip_signal = pyqtSignal(object, str, bool)

    def __init__(self, audio_service: AudioControlService):
        super().__init__()
        self.audio_service = audio_service
        self.settings = QSettings("MicControl", "MicrophoneControlApp")
        self.current_device = None

        self.setWindowTitle("Control de Micrófono")
        self.setGeometry(100, 100, 500, 400)

        # Deshabilitar la maximización de la ventana
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.alert_widget = AlertWidget(self)
        self.layout.addWidget(self.alert_widget)
        self.alert_widget.hide()

        self.init_ui()
        self.load_settings()
        self.init_tray()

        self.tooltip = VolumeTooltip(self)
        self.tooltip_timer = QTimer(self)
        self.tooltip_timer.timeout.connect(self.tooltip.hide)

        self.update_tooltip_signal.connect(self.update_tooltip)

        # Obtener iconos del sistema
        self.style = self.style()
        self.mic_on_icon = self.style.standardIcon(QStyle.SP_MediaVolume)
        self.mic_off_icon = self.style.standardIcon(QStyle.SP_MediaVolumeMuted)

    def show_alert(self, message, alert_type="error"):
        self.alert_widget.show_alert(message, alert_type)

    def init_ui(self):
        # Grupo de Configuración de Micrófono
        mic_group = QGroupBox("Configuración de Micrófono")
        mic_layout = QVBoxLayout()

        # Selector de micrófono
        mic_selection_layout = QHBoxLayout()
        mic_selection_layout.addWidget(QLabel("Micrófono:"))
        self.mic_combo = QComboBox()
        self.update_microphone_list()
        self.mic_combo.currentTextChanged.connect(self.update_current_device)
        mic_selection_layout.addWidget(self.mic_combo)
        mic_selection_layout.addStretch(1)
        mic_layout.addLayout(mic_selection_layout)

        # Control de volumen
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Paso de volumen:"))
        self.vol_step = QSpinBox()
        self.vol_step.setRange(1, 20)
        self.vol_step.setValue(5)
        self.vol_step.setFixedWidth(50)
        vol_layout.addWidget(self.vol_step)
        vol_layout.addStretch(1)
        mic_layout.addLayout(vol_layout)

        mic_group.setLayout(mic_layout)
        self.layout.addWidget(mic_group)

        # Grupo de Atajos de Teclado
        hotkey_group = QGroupBox("Atajos de Teclado")
        hotkey_layout = QVBoxLayout()

        self.volume_up_input = KeySequenceEdit()
        self.volume_down_input = KeySequenceEdit()
        self.mute_toggle_input = KeySequenceEdit()

        for action, widget in [
            ("Subir volumen", self.volume_up_input),
            ("Bajar volumen", self.volume_down_input),
            ("Alternar silencio", self.mute_toggle_input),
        ]:
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"{action}:"))
            layout.addWidget(widget)
            hotkey_layout.addLayout(layout)
            widget.key_sequence_changed.connect(self.on_key_sequence_changed)
            widget.capture_state_changed.connect(self.update_capture_buttons_state)

        hotkey_group.setLayout(hotkey_layout)
        self.layout.addWidget(hotkey_group)

        # Botón para guardar configuración
        self.save_button = QPushButton("Guardar configuración")
        save_button_font = QFont()
        save_button_font.setPointSize(12)  # Aumentar el tamaño de la fuente
        save_button_font.setBold(True)  # Hacer la fuente negrita
        self.save_button.setFont(save_button_font)
        self.save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.update_save_button_style(True)

    def update_microphone_list(self):
        self.mic_combo.clear()
        devices = self.audio_service.get_input_devices()
        for device in devices:
            self.mic_combo.addItem(device.name, device)

    def load_settings(self):
        saved_mic = self.settings.value("microphone", "")
        index = self.mic_combo.findText(saved_mic)
        if index >= 0:
            self.mic_combo.setCurrentIndex(index)
        self.vol_step.setValue(int(self.settings.value("volume_step", 5)))
        self.volume_up_input.set_key_sequence(
            self.settings.value("volume_up_hotkey", "")
        )
        self.volume_down_input.set_key_sequence(
            self.settings.value("volume_down_hotkey", "")
        )
        self.mute_toggle_input.set_key_sequence(
            self.settings.value("mute_toggle_hotkey", "")
        )
        self.update_current_device()
        self.apply_hotkeys()

    def save_settings(self):
        self.settings.setValue("microphone", self.mic_combo.currentText())
        self.settings.setValue("volume_step", self.vol_step.value())
        self.settings.setValue(
            "volume_up_hotkey", self.volume_up_input.get_key_sequence()
        )
        self.settings.setValue(
            "volume_down_hotkey", self.volume_down_input.get_key_sequence()
        )
        self.settings.setValue(
            "mute_toggle_hotkey", self.mute_toggle_input.get_key_sequence()
        )
        self.settings.sync()
        self.apply_hotkeys()
        self.show_alert("La configuración se ha guardado correctamente.", "success")

    def update_current_device(self):
        index = self.mic_combo.currentIndex()
        if index >= 0:
            self.current_device = self.mic_combo.itemData(index)
        else:
            self.current_device = None

    def volume_up(self):
        if self.current_device:
            try:
                new_volume, is_muted = self.audio_service.volume_up(
                    self.current_device, self.vol_step.value() / 100
                )
                self.update_tooltip_signal.emit(new_volume, None, is_muted)
            except Exception as e:
                self.show_alert(str(e))

    def volume_down(self):
        if self.current_device:
            try:
                new_volume, is_muted = self.audio_service.volume_down(
                    self.current_device, self.vol_step.value() / 100
                )
                self.update_tooltip_signal.emit(new_volume, None, is_muted)
            except Exception as e:
                self.show_alert(str(e))

    def mute_toggle(self):
        if self.current_device:
            try:
                is_muted = self.audio_service.toggle_mute(self.current_device)
                status = "silenciado" if is_muted else "activado"
                self.update_tooltip_signal.emit(None, status, is_muted)
            except Exception as e:
                self.show_alert(str(e))

    def update_tooltip(self, volume=None, status=None, is_muted=False):
        icon = self.mic_off_icon if is_muted else self.mic_on_icon
        if volume is not None:
            step = self.vol_step.value()
            volume_percentage = round(volume * 100 / step) * step
            text = f"Volumen: {volume_percentage}%"
        elif status is not None:
            text = f"Micrófono {status}"
        else:
            return

        self.tooltip.show_tooltip(text, icon)
        self.tooltip_timer.start(1500)

    def apply_hotkeys(self):
        keyboard.unhook_all()
        for action in ["volume_up", "volume_down", "mute_toggle"]:
            hotkey = getattr(self, f"{action}_input").get_key_sequence()
            if hotkey:
                try:
                    keyboard_hotkey = self.convert_to_keyboard_hotkey(hotkey)
                    keyboard.add_hotkey(keyboard_hotkey, getattr(self, action))
                    print(f"Atajo configurado para {action}: {keyboard_hotkey}")
                except ValueError as e:
                    print(f"Error al configurar el atajo para {action}: {e}")

    def convert_to_keyboard_hotkey(self, qt_hotkey):
        modifiers_map = {
            "Ctrl": "ctrl",
            "Alt": "alt",
            "Shift": "shift",
            "Meta": "win",
        }

        keys = qt_hotkey.split("+")
        keyboard_keys = []

        for key in keys:
            key = key.strip()
            if key in modifiers_map:
                keyboard_keys.append(modifiers_map[key])
            elif key in ["÷", "="]:
                keyboard_keys.append("=")
            elif key == "_":
                keyboard_keys.append("-")
            else:
                keyboard_keys.append(key.lower())

        return "+".join(keyboard_keys)

    def update_capture_buttons_state(self, is_capturing):
        capturing_input = None
        for input_widget in [
            self.volume_up_input,
            self.volume_down_input,
            self.mute_toggle_input,
        ]:
            if input_widget.is_capturing:
                capturing_input = input_widget
                break

        for input_widget in [
            self.volume_up_input,
            self.volume_down_input,
            self.mute_toggle_input,
        ]:
            if input_widget != capturing_input:
                input_widget.set_capture_button_enabled(not is_capturing)

        self.update_save_button_style(not is_capturing)

    def update_save_button_style(self, enabled):
        self.save_button.setEnabled(enabled)
        if enabled:
            self.save_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                """
            )
        else:
            self.save_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #bdc3c7;
                    color: #7f8c8d;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                }
                """
            )

    def on_key_sequence_changed(self, key_sequence):
        pass

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Mostrar", self)
        quit_action = QAction("Salir", self)
        hide_action = QAction("Ocultar", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit_application)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Microphone Control",
            "La aplicación sigue ejecutándose en segundo plano.",
            QSystemTrayIcon.Information,
            2000,
        )

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.instance().quit()
