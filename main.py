import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    # reads .env file so GEMINI_API_KEY is available via os.environ
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

    # wrap the prompt in the Content format the API expects; this list grows as tool results are appended
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]
    verbose = args.verbose

    response = generate_content(client, messages, verbose)
    execute_tool_calls(response, verbose) if response else None

# Runs one agentic turn: sends messages, handles any tool calls, then returns.
# Feed function_results back into messages and call again to continue the loop.
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
        # response.text is set when the model gives a final answer with no tool calls
        if response.text:
            print(response.text)
        return response

    # Catch API errors, especially rate limits
    except errors.ClientError as e:
        if "429" in str(e):
            print("Rate limit exceeded. Please try again later.")
        else:
            print("Client error:", e)


def execute_tool_calls(response, verbose=False):
    # response.function_calls is set when the model wants to invoke one or more tools
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_response = call_function(function_call, verbose)

            if not function_response.parts:
                raise RuntimeError("No function response parts received")
            # unwrap the nested structure: Content -> Part -> FunctionResponse
            fr = function_response.parts[0].function_response
            if fr is None:
                raise RuntimeError("No function response received")
            if fr.response is None:
                raise RuntimeError("No response payload received")
            # collect each tool result to append to messages for the next turn
            function_results.append(function_response.parts[0])
            if verbose:
                print(f"-> {fr.response}")


if __name__ == "__main__":
    main()
