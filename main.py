import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from collections import deque

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")



if api_key is None:
    raise RuntimeError("invalid key")



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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
                else:
                    continue
            elif command == "history":
                history_list = list(messages)
                for i in range(0, len(history_list), 2):
                    prompt_number = i // 2 + 1
                    user_message = history_list[i]
                    assistant_message = history_list[i + 1]
                    print(f"----------Prompt #{prompt_number}----------")
                    print(f"You: {user_message["content"]}")
                    print(f"Assistant: {assistant_message["content"]}")
                    print("----------------------------------")
            else:
                print(f"Command not found: /{command}")
                continue
        messages.append({"role": "user", "content": user_input})
        full_messages = system_message + list(messages)
        response = client.chat.completions.create(model=model, messages=full_messages)
        reply = response.choices[0].message.content
        print(f"Z: {reply}")
        messages.append({"role": "assistant", "content": reply})
        if args.verbose:
            print(f"User input: {user_input}")


main()

