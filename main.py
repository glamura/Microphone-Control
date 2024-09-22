import sys
import platform
from src.application.services.audio_control_service import AudioControlService

if platform.system() == "Windows":
    from PyQt5.QtWidgets import QApplication
    from src.interfaces.gui.main_window import MicrophoneControlGUI
    from src.infrastructure.adapters.pycaw_audio_adapter import (
        PycawAudioAdapter as AudioAdapter,
    )
else:
    from src.interfaces.cli.cli_interface import CLIInterface
    from src.infrastructure.adapters.generic_audio_adapter import (
        GenericAudioAdapter as AudioAdapter,
    )


def main():
    audio_adapter = AudioAdapter()
    audio_service = AudioControlService(audio_adapter)

    if platform.system() == "Windows":
        app = QApplication(sys.argv)
        window = MicrophoneControlGUI(audio_service)

        if "--minimized" not in sys.argv:
            window.show()

        sys.exit(app.exec_())
    else:
        cli = CLIInterface(audio_service)
        cli.run()


if __name__ == "__main__":
    main()
