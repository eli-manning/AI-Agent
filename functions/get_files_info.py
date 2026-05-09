import os
from functions.validate_path import validate_path
from google.genai import types

def get_files_info(working_directory, directory="."):
    target_dir, error = validate_path(working_directory, directory)
    if error:
        return error
    try:
        files_info = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            size_bytes = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            files_info.append(
                f'- {item}: file_size={size_bytes} bytes, is_dir={is_dir}')
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
