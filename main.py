import os
import argparse
import json
from constants import AVAILABLE_MODELS, COMMAND_HELP
from dotenv import load_dotenv
from openai import OpenAI
from collections import deque
from features.files_information import search_content, list_directory
from features.functions import read_files, create_and_edit_files, read_images, convert_codingfile, bookbot
from ui import show_message
from rich.panel import Panel
from rich.console import Console
from rich.table import Table


FUNCTION_MAP = {
    "list_directory": list_directory,
    "search_content": search_content,
    "read_files": read_files,
    "create_and_edit_files": create_and_edit_files,
    "read_images": read_images,
    "convert_codingfile": convert_codingfile,
    "bookbot": bookbot
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists all files and subdirectories inside a given directory path within the user's home directory. Use this when the user wants to see what's inside a folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list contents of, relative to or within the home directory."
                    }
                },
                "required": ["path"]
            }
        }
    },
        {
    "type": "function",
    "function": {
        "name": "search_content",
        "description": "Searches for files or directories by name anywhere within the user's home directory, recursively. Use this when the user wants to find something but doesn't know its exact location.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name (or partial name) of the file or directory to search for."
                }
            },
            "required": ["name"]
        }
      }
    },
    {
    "type": "function",
    "function": {
        "name": "read_files",
        "description": "Reads and returns the content of a text-based file (.txt, .py, .md, .c, .sh, .go, .pdf) within the user's home directory. Use this when the user wants to see, summarize, or analyze the contents of a specific file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The path to the file to read, relative to or within the home directory."
                },
                "num_lines": {
                    "type": "integer",
                    "description": "Optional. If provided, only reads this many lines from the start of the file instead of the entire file."
                }
            },
            "required": ["file"]
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_and_edit_files",
        "description": "Creates a new file or edits an existing file within the user's home directory. Use mode='create' to make a brand-new file (fails if it already exists). Use mode='edit' to append content to an existing file (fails if the file doesn't exist).",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The path to the file to create or edit, relative to or within the home directory."
                },
                "mode": {
                    "type": "string",
                    "enum": ["create", "edit"],
                    "description": "Whether to create a new file or edit an existing one."
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file. Required for 'edit' mode; ignored for 'create' mode."
                }
            },
            "required": ["file", "mode"]
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "read_images",
        "description": "Reads and encodes an image file (.png, .jpg, .jpeg) from within the user's home directory so it can be analyzed or described. Use this when the user wants you to look at, describe, or analyze a specific image file.",
        "parameters": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "description": "The path to the image file, relative to or within the home directory."
                }
            },
            "required": ["image"]
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "convert_codingfile",
        "description": "Converts a self-contained coding problem solution (like a LeetCode or Codewars style solution) from one language to another. Supports .py, .c, .go, .sh source files. Only works on self-contained algorithmic code with no file I/O, external libraries, or interactive input.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The path to the source code file to convert, relative to or within the home directory."
                },
                "target_language": {
                    "type": "string",
                    "enum": ["python", "go", "c", "shell"],
                    "description": "The language to convert the code into."
                }
            },
            "required": ["filepath", "target_language"]
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "bookbot",
        "description": "Analyzes a text file (.txt or .md) within the user's home directory and returns word count and character count statistics. Use this when the user wants to know how many words or characters are in a specific file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The path to the text file to analyze, relative to or within the home directory."
                }
            },
            "required": ["file"]
        }
    }
}
]


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
console = Console(force_terminal=True, color_system="truecolor")


if api_key is None:
    raise RuntimeError("invalid key")



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--tui", action="store_true", help="Enable rich-styled TUI output")
    args = parser.parse_args()

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
    model = "openrouter/free"
    system_message = [
         {      
            "role": "system",
            "content": "You are Z, an AI that can read and analyze files (.txt, .py, .md, .c, and .sh). You can also solve math problems ranging from Algebra to Pre-Calculus and count a file's total number of characters and words",
        },
    ]

    messages = deque(maxlen=25) 

    print("Welcome to Z! How may I help you?")
    while True:
        user_input = input().strip()

        if user_input.startswith("/"):
            command, *cmd_args = user_input[1:].split(" ")

            if command == "exit":
                confirmation = input("Are you sure you want to exit? Y or N. ").strip()
                if confirmation == "Y":
                    print("Exited Successfully!")
                    break
                elif confirmation == "N":
                    continue
                else:
                    print("Invalid input.")
                    continue
            elif command == "history":
                history_list = list(messages)
                for i in range(0, len(history_list), 2):
                    prompt_number = i // 2 + 1
                    user_message = history_list[i]
                    assistant_message = history_list[i + 1]

                    if args.tui:
                        content = f"[bold]You:[/bold] {user_message['content']}\n[bold cyan]Z:[/bold cyan] {assistant_message['content']}"
                        console.print(Panel(content, title=f"Prompt #{prompt_number}"))
                    else:
                        print(f"-------------Prompt #{prompt_number}-------------")
                        print(f"You: {user_message["content"]}")
                        print(f"Assistant: {assistant_message["content"]}")
                        print("-----------------------------------")
                continue
            elif command =="list":
                path = " ".join(cmd_args)
                result = list_directory(path)
                if result["status"]:
                    if args.tui:
                        table = Table(title=result["message"])
                        table.add_column("Item")
                        for item in result["contents"]:
                            table.add_row(str(item))
                        console.print(table)
                    else:
                        print(result["message"])
                        for item in result["contents"]:
                            print(f"  {item}")
                else:
                    show_message(result["message"], tui_mode=args.tui, style="red")
                continue
            elif command == "search":
                name = " ".join(cmd_args)
                result = search_content(name)
                if result["found"]:
                    if args.tui:
                        table = Table(title=result["status"])
                        table.add_column("Match")
                        for match in result["matches"]:
                            table.add_row(str(match))
                        console.print(table)
                    else:
                        print(result["status"])
                        for match in result["matches"]:
                            print(f"  {match}")
                else:
                    show_message(result["status"], tui_mode=args.tui, style="red")
                continue
            elif command == "verbose":
                args.verbose = not args.verbose
                print(f"Verbose mode is now {'ON' if args.verbose else 'OFF'}.")
                continue
            elif command == "tui":
                args.tui = not args.tui
                print(f"TUI mode is now {'ON' if args.tui else 'OFF'}.")
                continue
            elif command == "model":
                alias = " ".join(cmd_args).strip()
                if alias in AVAILABLE_MODELS:
                    model = AVAILABLE_MODELS[alias]
                    print(f"Model switched to: {model}")
                else:
                    print(f"Unknown model alias: '{alias}'. Available: {', '.join(AVAILABLE_MODELS.keys())}")   
                continue
            elif command == "help":
                print("Available commands:")
                for cmd, description in COMMAND_HELP.items():
                    print(f"  /{cmd} — {description}")
                continue
            else:
                print(f"Command not found: /{command}")
                continue
        messages.append({"role": "user", "content": user_input})
        full_messages = system_message + list(messages)
        response = client.chat.completions.create(model=model, messages=full_messages, tools=tools)
        reply_message = response.choices[0].message
        if args.verbose:
            print(f"[debug] tool_calls: {reply_message.tool_calls}")
            print(f"User input: {user_input}")
        if reply_message.tool_calls:
            messages.append({"role": "assistant", "content": reply_message.content, "tool_calls": reply_message.tool_calls})
            image_involved = False
            for tool_call in reply_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in FUNCTION_MAP:
                    if args.verbose:
                        print(f"[debug] Calling {function_name} with {function_args}")
                    if function_name == "read_images":
                        result = read_images(**function_args)
                        if result["verification_status"]:
                            image_involved = True
                            image_message = {
                                 "role": "user",
                                 "content": [
                                    {"type": "text", "text": "Here is the image to analyze."},
                                    {"type": "image_url", "image_url": {"url": f"data:{result['mime_type']};base64,{result['encoded_data']}"}}
                                ]
                            }
                            messages.append(image_message)
                        else:
                             messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, default=str)})
                    elif function_name == "convert_codingfile":
                         result = convert_codingfile(**function_args, client=client, model=model)
                         messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, default=str)})
                    else:
                        result = FUNCTION_MAP[function_name](**function_args)
                        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, default=str)})
                else:
                    result = {"error": f"Unknown function: {function_name}"}
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, default=str)})

                if args.verbose:
                    print(f"[debug] Result: {result}")

            full_messages = system_message + list(messages)
            call_model = AVAILABLE_MODELS["vision"] if image_involved else model
            final_response = client.chat.completions.create(model=call_model, messages=full_messages)
            final_reply = final_response.choices[0].message.content
            show_message(f"Z: {final_reply}", tui_mode=args.tui, style="cyan")
            messages.append({"role": "assistant", "content": final_reply})
        else:
            reply = response.choices[0].message.content
            show_message(f"Z: {reply}", tui_mode=args.tui, style="cyan")
            messages.append({"role": "assistant", "content": reply})



main()

