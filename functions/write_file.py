from functions.validate_path import validate_path
import os

def write_file(working_directory, file_path, content):
    target, error = validate_path(working_directory, file_path, writing=True)
    if error:
        return error
    try:
        parent_dir = os.path.dirname(target)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"