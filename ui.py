from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from theme import custom_theme, COLORS
import time

class TerminalUI:
    def __init__(self, mode, os_type):
        self.console = Console(theme=custom_theme)
        self.mode = mode
        self.os_type = os_type
        self.spinner = None

    def update_mode(self, mode):
        self.mode = mode

    def clear(self):
        self.console.clear()

    def welcome_screen(self):
        self.clear()
        title = Text(" NL-Terminal v2.0 ", style="panel.title")
        subtitle = Text(f"Mode: {self.mode.upper()}  |  OS: {self.os_type}", style="comment")
        
        welcome_panel = Panel(
            Text.assemble(
                ("\nWelcome to the Future of Command Line Interfaces.\n", "info"),
                ("Type 'help' or anything in natural language to get started.\n", "foreground"),
                justify="center"
            ),
            title=title,
            subtitle=subtitle,
            border_style="panel.border",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)
        self.console.print(Rule(style="comment"))
        self.console.print()

    def get_input(self):
        # Create a visually distinct prompt
        mode_style = "prompt"
        if self.mode == "expert": mode_style = "red"
        elif self.mode == "safe": mode_style = "green"
        
        return Prompt.ask(f"[{mode_style}]➜ {self.mode.upper()}[/{mode_style}]")

    def print_command_execution(self, command):
        self.console.print(f"[comment]Executing:[/comment] [command]{command}[/command]")

    def print_ai_thinking(self):
        self.spinner = self.console.status("[ai.thinking]AI is thinking...[/ai.thinking]", spinner="dots")
        self.spinner.start()

    def stop_ai_thinking(self):
        if self.spinner:
            self.spinner.stop()
            self.spinner = None

    def print_ai_response(self, text):
        self.stop_ai_thinking()
        panel = Panel(
            text,
            title="[ai.thinking]AI Knowledge[/ai.thinking]",
            border_style="purple",
            expand=False
        )
        self.console.print(panel)

    def print_error(self, message):
        self.stop_ai_thinking()
        self.console.print(f"[error]✖ Error:[/error] {message}")

    def print_success(self, message):
        self.stop_ai_thinking()
        self.console.print(f"[success]✔ Success:[/success] {message}")

    def print_info(self, message):
        self.console.print(f"[info]ℹ Info:[/info] {message}")

    def print_warning(self, message):
        self.console.print(f"[warning]⚠ Warning:[/warning] {message}")

    def stream_output(self, output):
        # Determine if output looks like a list or table, otherwise just print
        self.console.print(output, style="foreground")

