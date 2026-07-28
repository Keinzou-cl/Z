# Z

Z is a personal AI agent that's built from scratch in Python. It combines a conversational LLM (via [OpenRouter](https://openrouter.ai)) with a set of tools for working with your local files — reading, writing, searching, converting code, analyzing images, and more — all gated behind a path-safety layer that keeps operations sandboxed to your home directory.

Z runs as a CLI, with an optional `rich`-powered TUI display mode.

## What Z can do

- **Read, write, and edit files** — plain text (`.txt`, `.py`, `.md`, `.c`, `.sh`, `.go`) and PDFs
- **Count words and characters** in a text file
- **Remember conversation history** — up to 25 messages, oldest automatically dropped
- **Convert code between languages** — self-contained algorithmic solutions (LeetCode/Codewars-style) between Python, Go, C, and Shell
- **Analyze images** — reads and encodes `.png`/`.jpg`/`.jpeg` files for vision-capable models
- **Create files** in any directory within your home folder
- **Built-in commands** for quick, direct actions without going through the LLM (see below)
- **Switch models** on the fly
- **Validate every filepath** before touching it — checks it's inside your home directory and reports whether it's safe or "dangerous"
- **List directory contents**, gated behind the same validation
- **Tool-calling** — the LLM can decide on its own to invoke any of the above based on natural conversation, not just slash commands

## Requirements

- Python 3.13+
- An [OpenRouter](https://openrouter.ai) API key (free tier available)
- [`uv`](https://docs.astral.sh/uv/) (recommended) — or `pip`, if you prefer
- python-dotenv → Loading OPENROUTER_API_KEY from .env
- pypdf → 	Extracting text from .pdf files in read_files
- rich → The TUI display mode (--tui)

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Z
```

### 2. Install dependencies

**Using `uv` (recommended):**
```bash
uv sync
```

**Using `pip`:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root:
```bash
OPENROUTER_API_KEY=your_api_key_here
```

## Running Z

**Using `uv` (recommended):**
```bash
uv run main.py
```

**Using the launch script:**
```bash
./main.sh
```

**Using `pip`/`venv` directly:**
```bash
python3 main.py
```

### Flags

| Flag | Description |
|------|--------------|
| `--verbose` | Print debug info, including tool calls and their raw results |
| `--tui` | Enable `rich`-styled colored/table output instead of plain text |

Example:
```bash
uv run main.py --tui --verbose
```

## Built-in commands

Type these directly in the chat (they're handled instantly, without calling the LLM):

| Command | Description |
|---------|-------------|
| `/exit` | Exit the program (asks for confirmation) |
| `/history` | Show the current conversation history |
| `/list <path>` | List the contents of a directory |
| `/search <name>` | Search your home directory for a file or folder by name |
| `/model <alias>` | Switch the active model |
| `/verbose` | Toggle verbose mode on/off |
| `/tui` | Toggle TUI mode on/off |
| `/help` | Show all available commands |


Anything else you type is sent to the LLM, which can choose to call any of Z's tools on its own based on what you ask for.

## Project structure

```
Z/
├── main.py                        # Entry point, CLI loop, router, tool-calling logic
├── ui.py                          # rich-based display helpers (TUI mode)
├── constants.py                   # Shared constants (HOME_DIR, model aliases, etc.)
├── features/
│   ├── files_information.py       # Path validation, directory listing, search, file read/write, image reading
│   └── functions.py                # Additional supporting functions
└── pyproject.toml / uv.lock         # uv dependency management
```

## Notes

- All file operations are restricted to your home directory — anything outside it is flagged as unsafe and refused.
- Z uses free-tier models by default. Free models on OpenRouter have daily rate limits and can occasionally be unavailable or change without notice.
- Image analysis requires a vision-capable model — switch to one via `/model` before asking Z to look at an image.
