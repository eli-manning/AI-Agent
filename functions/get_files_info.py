import os


def get_files_info(working_directory, directory="."):
    try:
        working_absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_absolute, directory))
        valid_target_dir = os.path.commonpath(
            [working_absolute, target_dir]) == working_absolute
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.exists(target_dir):
            return f'Error: "{directory}" is not a directory'

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
