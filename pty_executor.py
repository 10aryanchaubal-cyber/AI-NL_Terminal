import os
import sys
import shlex
import subprocess

def run_interactive(command):
    """
    Runs interactive commands.
    - POSIX: uses PTY
    - Windows: falls back to native shell
    """
    if os.name == "posix":
        try:
            import pty
            argv = shlex.split(command)
            pty.spawn(argv)
        except Exception as e:
            print(f"PTY execution failed: {e}")
    else:
        # Windows fallback: run command directly in shell
        # CONNECT STREAMS to allow interactivity (vim, python, etc)
        try:
            subprocess.run(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        except Exception as e:
            print(f"Interactive execution failed: {e}")
