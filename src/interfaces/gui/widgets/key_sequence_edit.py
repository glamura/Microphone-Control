from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence


class KeySequenceEdit(QWidget):
    key_sequence_changed = pyqtSignal(str)
    capture_state_changed = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit(self)
        self.line_edit.setReadOnly(True)
        self.layout.addWidget(self.line_edit)

        self.capture_button = QPushButton("Capturar", self)
        self.capture_button.clicked.connect(self.toggle_capture_mode)
        self.layout.addWidget(self.capture_button)

        self.is_capturing = False
        self.key_sequence = []

        self.update_styles()

    def update_styles(self):
        base_style = """
            QLineEdit {
                border: 2px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
                background-color: #F0F0F0;
                font-size: 14px;
            }
        """
        capture_style = """
            QLineEdit {
                border-color: #e74c3c;
                background-color: #FADBD8;
            }
        """
        button_style = """
            QPushButton {
                font-size: 14px;
                padding: 5px 10px;
                border: none;
                border-radius: 5px;
            }
        """
        button_capture_style = """
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        button_normal_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

        self.line_edit.setStyleSheet(
            base_style + (capture_style if self.is_capturing else "")
        )
        self.capture_button.setStyleSheet(
            button_style
            + (button_capture_style if self.is_capturing else button_normal_style)
        )

    def set_capture_button_enabled(self, enabled):
        self.capture_button.setEnabled(enabled)
        self.update_styles()

    def toggle_capture_mode(self):
        self.is_capturing = not self.is_capturing
        if self.is_capturing:
            self.line_edit.clear()
            self.key_sequence = []
            self.capture_button.setText("Detener")
            self.line_edit.setPlaceholderText("Presione las teclas...")
        else:
            self.capture_button.setText("Capturar")
            self.line_edit.setPlaceholderText("")
        self.update_styles()
        self.capture_state_changed.emit(self.is_capturing)

    def keyPressEvent(self, event):
        if not self.is_capturing:
            return super().keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.toggle_capture_mode()
            return

        modifiers = event.modifiers()
        key = event.key()

        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return

        key_string = QKeySequence(key).toString()

        modifiers_text = []
        if modifiers & Qt.ControlModifier:
            modifiers_text.append("Ctrl")
        if modifiers & Qt.AltModifier:
            modifiers_text.append("Alt")
        if modifiers & Qt.ShiftModifier:
            modifiers_text.append("Shift")
        if modifiers & Qt.MetaModifier:
            modifiers_text.append("Meta")

        full_key_sequence = "+".join(modifiers_text + [key_string])
        self.line_edit.setText(full_key_sequence)
        self.key_sequence_changed.emit(full_key_sequence)

    def set_key_sequence(self, sequence):
        self.line_edit.setText(sequence)

    def get_key_sequence(self):
        return self.line_edit.text()
