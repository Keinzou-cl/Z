from rich.console import Console

console = Console(force_terminal=True, color_system="truecolor")

def show_message(text, tui_mode=False, style=None):
    if tui_mode:
        console.print(text, style=style)
    else:
        print(text)