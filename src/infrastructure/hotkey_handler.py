from pynput import keyboard


class HotkeyHandler:
    def __init__(self):
        self.hotkeys = {}
        self.listener = None

    def add_hotkey(self, key_combination, callback):
        self.hotkeys[self.parse_key_combination(key_combination)] = callback

    def start_listening(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_listening(self):
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
        try:
            key_combination = frozenset([key])
            if key_combination in self.hotkeys:
                self.hotkeys[key_combination]()
        except AttributeError:
            pass

    def parse_key_combination(self, combination):
        keys = combination.lower().split("+")
        return frozenset(
            getattr(keyboard.Key, key, keyboard.KeyCode.from_char(key)) for key in keys
        )


hotkey_handler = HotkeyHandler()
