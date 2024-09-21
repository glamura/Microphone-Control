from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer


class AlertWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setFixedHeight(50)
        self.hide()

    def show_alert(self, message, alert_type="error", duration=3000):
        if alert_type == "error":
            style = """
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            """
        elif alert_type == "success":
            style = """
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            """
        else:
            style = """
                background-color: #fff3cd;
                color: #856404;
                border: 1px solid #ffeeba;
            """

        self.setStyleSheet(
            style
            + """
            border-radius: 4px;
            padding: 10px;
        """
        )

        self.label.setText(message)
        self.show()
        QTimer.singleShot(duration, self.hide)
