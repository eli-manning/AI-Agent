from functions.validate_path import validate_path
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    target, error = validate_path(working_directory, file_path, check_is_file=True)
    if error:
        return error
    try:
        with open(target, "r") as f:
            content = f.read(MAX_CHARS)
            # read one extra byte to detect truncation without loading the whole file
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file at the specified path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
