from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import prompt as sub_prompt
from prompt_toolkit.styles import Style as kitStyle

from core import *


class FouineConsole:
    def __init__(self):
        self.MAIN_COMMANDS = ["list-partitions", "list-fs", "ls"]
        self.fouine = Fouine(
            "/home/njord/Desktop/Devs/2600/FOR/code/2600_Forensic_Tool/disks/disk.E01"
        )
        self.history = FileHistory(".history")
        self.key_bindings = KeyBindings()
        self.style = kitStyle.from_dict(
            {"prompt": "ansired bold", "command": "ansigreen", "output": "ansiwhite"}
        )
        self.completer = WordCompleter(self.MAIN_COMMANDS)
        self.prompt_template = "{style.prompt}[FOUINER] > {style.command}"

        # Set up key bindings
        @self.key_bindings.add("c-c")
        @self.key_bindings.add("c-d")
        def _(event):
            raise KeyboardInterrupt

    def prompt_callback(self, text):
        if text == "exit":
            raise EOFError
        else:
            self.execute_command(text)

    def execute_command(self, command):
        # Handle main commands
        if command == "list-partitions":
            print(f"Listing partitions ...")
            print(self.fouine.partition_table)
        if command == "list-fs":
            print("Listing filesystems")
            print(self.fouine.partition_table._list_vol_fs())
        if command == "ls":
            pass
        else:
            print(f"Executing command {command} can't be achieved cause not deinfed ...")

    def run(self):
        with patch_stdout():
            while True:
                try:
                    text = prompt(
                        self.prompt_template.format(style=self.style),
                        history=self.history,
                        key_bindings=self.key_bindings,
                        style=self.style,
                        completer=None,
                    )
                    self.prompt_callback(text)
                except EOFError:
                    break
                except KeyboardInterrupt:
                    continue


if __name__ == "__main__":
    prompt_instance = FouineConsole()
    prompt_instance.run()
