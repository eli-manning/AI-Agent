from functions.validate_path import validate_path
import os
from google.genai import types

def write_file(working_directory, file_path, content):
    target, error = validate_path(working_directory, file_path, writing=True)
    if error:
        return error
    try:
        parent_dir = os.path.dirname(target)
        # dirname returns '' for bare filenames; makedirs('') raises an error
        if parent_dir:
            # exist_ok avoids an error when the directory already exists
            os.makedirs(parent_dir, exist_ok=True)
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"

# schema tells the model what this function does and what arguments it accepts
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
