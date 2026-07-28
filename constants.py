from pathlib import Path

# For main.py:
AVAILABLE_MODELS = {
    "free": "openrouter/free",
    "qwen-vl": "qwen/qwen2.5-vl-32b-instruct:free",
    "vision": "google/gemma-4-31b-it:free",
}

COMMAND_HELP = {
    "exit": "Exit the program. Asks for confirmation before quitting.",
    "history": "Show the current conversation history (up to 25 messages).",
    "list": "/list <path> — List the contents of a directory.",
    "search": "/search <name> — Search for files or folders by name.",
    "verbose": "Toggle verbose mode on/off.",
    "model": f"/model <alias> — Switch models. Available: {', '.join(AVAILABLE_MODELS.keys())}",
}



# For files_information.py:
HOME_DIR = Path.home()
EXCLUDED1 = [".venv", ".git", ".gitignore", ".env", "__pycache__", ".ssh", ".bash_logout", ".wget_hsts", ".claude", ".vscode-server", ".profile", ".local", ".config", ".bashrc", ".sudo_as_admin_successful", ".bash_history"]
EXCLUDED2 = [".cache", ".dotnet", ".gitconfig", ".lesshst", ".wget-hsts", ".motd-shown", ".bootdev-yaml", ".motd_shown", ".landscape", ".bootdev.yaml"]

# For functions.py:
AVAILABLE_FILETYPES = [".py", ".txt", ".pdf", ".md", ".c", ".sh", ".go"]
AVAILABLE_IMAGETYPES = [".jpeg", ".png", ".jpg"]
AVAILABLE_CODINGFILETYPES = [".py", ".c", ".go", ".sh"]
UNACCEPTABLE_PATTERNS = ["import os", "import sys", "import subprocess", "import socket", "open(", "input("]
CONVERSION_REFUSED = f'The contents of this file are not convertible or not supported as it may not be a problem-solving code.'