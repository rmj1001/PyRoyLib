import subprocess
import os

def pause() -> None:
    """Pause program execution"""
    _ = input("Press [ENTER] to continue...")

def clear() -> None:
    """Clear screen"""
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def ask(question: str) -> bool:
    """Ask a question and return true if case-insensitive answer is 'y' or 'yes'"""
    answer = input(f"{question} [y/N]: ").lower()
    return answer in ["y", "yes"]
