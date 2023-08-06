from pathlib import Path
from sphinx.errors import SphinxError


class XournalError(SphinxError):
    category = "Xournal Error"


class XournalCallError(SphinxError):
    category = "Xournal Error"

    def __init__(self, command: [str], error: int | OSError, stderr: str = "",
                 stdout: str = ""):
        self.command = command
        self.error = error
        self.stderr = stderr if stderr else ""
        self.stdout = stdout if stdout else ""
        message = "\n".join([
            f"Xournal exited with error: {error}",
            f"Command: {' '.join(command)}"
        ])

        if stderr and stdout:
            message = "\n".join([
                message,
                f"Trace:"
                f"{stdout}"
                f"{stderr}"
            ])

        super().__init__(message)
