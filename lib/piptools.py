import subprocess
import sys

class PipException(Exception):
    """Exception raised when pip command fails on console."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class PipHandler:
    """Handle pip commands on the console and install or require packages."""
    COMMANDS = [sys.executable, "-m", "pip"]

    @staticmethod
    def run(commands: list[str] | str):
        """Run a pip command from the command line. Raise PipException on failure."""
        commands = PipHandler.COMMANDS + [commands] if isinstance(commands, str) else PipHandler.COMMANDS + commands

        try:
            subprocess.check_call(commands)
        except subprocess.CalledProcessError as e:
            raise PipException(f"Command {' '.join(commands)} failed and returned a non-zero exit code.")

    @staticmethod
    def unrecoverable(message: str):
        """Print error to console and exit with status code 1."""
        print(f"PipHandler: {message}")
        sys.exit(1)

    @staticmethod
    def installed_packages() -> list[str]:
        """Returns a list of installed pip packages."""
        reqs = subprocess.check_output(PipHandler.COMMANDS + ['freeze'])
        return [r.decode().split('==')[0] for r in reqs.split()]

    @staticmethod
    def is_installed(package: str) -> bool:
        """Check if a package is installed."""
        return package in PipHandler.installed_packages()

    @staticmethod
    def install(packages: str | list[str]) -> None:
        """Try to install a pip package."""
        if isinstance(packages, str):
            if PipHandler.is_installed(packages):
                return

            try:
                PipHandler.run(["install", packages])
            except PipException:
                raise PipException(f"Failed to install package '{packages}'.")

        failed_packages = []

        for package in packages:
            if PipHandler.is_installed(package):
                continue

            try:
                PipHandler.run(["install", package])
            except PipException:
                failed_packages.append(package)

        if len(failed_packages) > 0:
            raise PipException(f"Failed to install packages: {', '.join(failed_packages)}.")

    @staticmethod
    def require(packages: str | list[str]) -> None:
        """Try to install one or more pip package(s), exit if package(s) not installed."""
        try:
            PipHandler.install(packages)
        except PipException as e:
            PipHandler.unrecoverable(e.message)
