import subprocess
import shlex
import os

INTERACTIVE_COMMANDS = {
    "vim", "nano", "top", "htop",
    "less", "more",
    "python", "python3",
    "bash", "sh", "zsh",
    "cmd", "powershell"
}

def is_interactive(command):
    try:
        parts = shlex.split(command)
        if not parts:
            return False
        return parts[0].lower() in INTERACTIVE_COMMANDS
    except Exception:
        return False


def execute(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout = result.stdout.decode("utf-8", errors="ignore")
        stderr = result.stderr.decode("utf-8", errors="ignore")

        return stdout, stderr

    except Exception as e:
        return "", str(e)
