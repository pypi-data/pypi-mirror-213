from pathlib import Path
from sphinx.errors import SphinxError


class XournalError(SphinxError):
    category = "Xournal Error"


class XournalCallError(SphinxError):
    category = "Xournal Error"

    def __init__(self, binary_path: str | Path, parameters: [str], error: int | OSError, stderr: str = "",
                 stdout: str = ""):
        self.binary_path = binary_path
        self.parameters = parameters
        self.error = error
        self.stderr = stderr if stderr else ""
        self.stdout = stdout if stdout else ""
        message = "\n".join([
            f"Xournal exited with error: {error}",
            f"Path: {binary_path}"
            f"Parameters: {' '.join(parameters)}"
        ])

        if stderr and stdout:
            message = "\n".join([
                message,
                f"Trace:\n"
                f"{stdout}\n"
                f"{stderr}\n"
            ])

        super().__init__(message)
