from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
                           schema_get_file_content, schema_run_python_file, schema_write_file],
)


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    # dispatch table avoids a long if/elif chain and makes adding new functions easy
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    function_name = function_call.name or ""
    if function_name not in function_map:
        # return the error as a tool response so the model can handle it gracefully
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # genai returns args as a MapComposite; convert to a plain dict for **kwargs unpacking
    args = dict(function_call.args) if function_call.args else {}
    # sandbox all tool calls to the calculator directory regardless of what the LLM requests
    args["working_directory"] = "./calculator"
    try:
        result = function_map[function_name](**args)
        # wrap result in the Content/Part format the API requires for tool responses
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )
