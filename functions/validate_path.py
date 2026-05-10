import os


# returns (resolved_absolute_path, None) on success, or (None, error_string) on failure
def validate_path(working_directory, path, check_is_file=False, writing=False, running=False):
    try:
        working_absolute = os.path.abspath(working_directory)
        # normpath collapses ../ components before we do the containment check
        target_path = os.path.normpath(os.path.join(working_absolute, path))

        # commonpath detects traversal attempts like ../../etc/passwd after normpath resolves them
        if os.path.commonpath([working_absolute, target_path]) != working_absolute:
            action = "write to" if writing else (
                "execute" if running else "access")
            return None, f'Error: Cannot {action} "{path}" as it is outside the permitted working directory'

        # writing creates the file, so a missing path is expected and fine
        if writing and os.path.isdir(target_path):
            return None, f'Error: Cannot write to "{path}" as it is a directory'

        if not writing and not os.path.exists(target_path):
            return None, f'Error: "{path}" does not exist'

        if not writing and check_is_file and not os.path.isfile(target_path):
            return None, f'Error: File not found or is not a regular file: "{path}"'

        # only allow executing .py files so the LLM can't run arbitrary binaries
        if running and not target_path.endswith(".py"):
            return None, f'Error: "{path}" is not a Python file'

        return target_path, None
    except Exception as e:
        return None, f"Error: {str(e)}"
