import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")



if api_key is None:
    raise RuntimeError("invalid key")



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
    model = "openrouter/free"
    messages = [
         {      
            "role": "system",
            "content": "You are Z, an AI that can read and analyze files (.txt, .py, .md, .c, and .sh). You can also solve math problems ranging from Algebra to Pre-Calculus and count a file's total number of characters and words",
        },
    {
        "role": "user",
        "content": args.user_prompt
    },
    ]
    

    response = client.chat.completions.create(model=model, messages=messages)


    print("=======================================")
    print(" ")
    print("Hello! Welcome to Z. An AI that can:")
    print(" ")
    print("✅ Read and Analyze files (.txt, .py, .md, .c, .sh)")
    print("✅ Solve Math Problems (from Algebra to Pre-Calculus)")
    print("✅ Count a File's Number of Characters and Words")
    print(" ")
    print("What can I do for you?")
    print("========================================")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    print(response.choices[0].message.content)

main()

