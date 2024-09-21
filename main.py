import sys
from PyQt5.QtWidgets import QApplication
from src.interfaces.gui.main_window import MicrophoneControlGUI
from src.application.services.audio_control_service import AudioControlService
from src.infrastructure.adapters.pycaw_audio_adapter import PycawAudioAdapter


def main():
    app = QApplication(sys.argv)

    audio_adapter = PycawAudioAdapter()
    audio_service = AudioControlService(audio_adapter)

    window = MicrophoneControlGUI(audio_service)

    if "--minimized" not in sys.argv:
        window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
