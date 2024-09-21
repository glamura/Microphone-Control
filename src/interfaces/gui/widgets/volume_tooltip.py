from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon


class VolumeTooltip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.layout = QHBoxLayout(self)
        self.icon_label = QLabel(self)
        self.text_label = QLabel(self)
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)
        self.setStyleSheet(
            """
            background-color: #F0F0F0;
            color: black;
            padding: 5px;
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            font-size: 12px;
        """
        )
        self.hide()

    def show_tooltip(self, text, icon=None):
        self.text_label.setText(text)
        if icon:
            # Ajusta el tamaño del icono según sea necesario
            self.icon_label.setPixmap(icon.pixmap(16, 16))
        else:
            self.icon_label.clear()
        self.adjustSize()
        cursor_pos = QCursor.pos()
        self.move(cursor_pos.x() + 15, cursor_pos.y() + 15)
        self.show()
