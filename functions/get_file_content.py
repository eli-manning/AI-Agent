from functions.validate_path import validate_path
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    target, error = validate_path(working_directory, file_path, check_is_file=True)
    if error:
        return error
    try:
        # initial read
        with open(target, "r") as f:
            content = f.read(MAX_CHARS)
            # check if extra content exists
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"