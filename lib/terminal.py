import os
import pathlib
import subprocess

import sys


class CLI:
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
    CLI.pause()
