import os
from functions.validate_path import validate_path

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
