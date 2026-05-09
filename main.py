import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
import argparse
from prompts import system_prompt
from functions.call_function import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]
    verbose = args.verbose

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose=False):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages,
            # temperature=0 for deterministic tool-call decisions
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))
        if response.usage_metadata is None:
            raise RuntimeError("Response is missing usage metadata")
        if verbose:
            print("User prompt:", messages[0].parts[0].text)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print(response.text)
        if response.function_calls:
            for function_call in response.function_calls:
                print(
                    f"Calling function: {function_call.name}({function_call.args})")

    # Catch API errors, especially rate limits
    except errors.ClientError as e:
        if "429" in str(e):
            print("Rate limit exceeded. Please try again later.")
        else:
            print("Client error:", e)


if __name__ == "__main__":
    main()
