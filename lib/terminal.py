import os
import pathlib
import subprocess
import sys


class CLI:
    """Command-line application helper class"""
    _author: str
    _copyright: int
    _commands: dict[str, str]
    _flags: dict[str, str]
    settings: dict

    def __init__(
            self,
            author: str,
            copyright: int,
            commands: dict[str, str] | None = None,
            flags: dict[str, str] | None = None,
            settings: dict | None = None
        ):
        self._author = author
        self._copyright = copyright

        # Add commands if any are passed
        if commands is None:
            self._commands = {}
        else:
            self._commands = commands

        # Add flags if any are passed
        if flags is None:
            self._flags = {}
        else:
            self._flags = flags

        # Add settings if any are passed
        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        # Add default help command
        self.add_command("help", "Show help message")

    def help(self) -> None:
        """Show help message with list of commands and flags with their descriptions"""
        print(f"{CLI.script_name()} - {self._author} (c) {self._copyright}")
        print()
        print("Commands:")

        for command, description in self._commands.items():
            print(f"\t{command}: {description}")

        print()
        print("Flags:")

        for flag, description in self._flags.items():
            print(f"\t{flag}: {description}")

    def add_command(self, name: str, description: str) -> None:
        """Add a command to the commands dictionary"""
        self._commands[name] = description

    def add_flag(self, name: str, description: str) -> None:
        """Add a flag to the flags dictionary"""
        self._flags[name] = description

    @staticmethod
    def args() -> list[str]:
        """Return list of command line arguments, excluding script path"""
        return sys.argv[1:]

    @staticmethod
    def script_dir() -> str:
        """Return script directory"""
        return str(pathlib.Path(__file__).parent.absolute())

    @staticmethod
    def script_name() -> str:
        """Return the name of the script"""
        return pathlib.Path(__file__).name

    @staticmethod
    def pause() -> None:
        """Pause program execution"""
        _ = input("Press [ENTER] to continue...")

    @staticmethod
    def clear() -> None:
        """Clear screen"""
        if os.name == "nt":
            subprocess.run("cls", shell=True)
        else:
            subprocess.run("clear", shell=True)

    @staticmethod
    def ask(question: str) -> bool:
        """Ask a question and return true if case-insensitive answer is 'y' or 'yes'"""
        answer = input(f"{question} [y/N]: ").lower()
        return answer in ["y", "yes"]


if __name__ == "__main__":
    """Testing"""
    print(f"File: {CLI.script_name()}")
    print(f"Dir: {CLI.script_dir()}")
    print(f"Args: {' '.join(CLI.args()) if len(CLI.args()) > 0 else 'None'}")

    print()

    # Testing CLI instance
    app = CLI("Roy Conn", 2026)
    app.add_flag("-s", "Empty")

    app.help()
