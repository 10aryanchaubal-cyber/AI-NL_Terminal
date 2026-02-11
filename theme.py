from rich.theme import Theme
from rich.style import Style

# Dracula-inspired theme
COLORS = {
    "background": "#282a36",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
}

custom_theme = Theme({
    "info": Style(color=COLORS["cyan"], bold=True),
    "warning": Style(color=COLORS["orange"], bold=True),
    "error": Style(color=COLORS["red"], bold=True, bgcolor=COLORS["background"]),
    "success": Style(color=COLORS["green"], bold=True),
    "prompt": Style(color=COLORS["green"], bold=True),
    "command": Style(color=COLORS["yellow"]),
    "ai.thinking": Style(color=COLORS["purple"], italic=True),
    "ai.response": Style(color=COLORS["foreground"]),
    "foreground": Style(color=COLORS["foreground"]),
    "comment": Style(color=COLORS["comment"]),
    "panel.border": Style(color=COLORS["purple"]),
    "panel.title": Style(color=COLORS["pink"], bold=True),
})
