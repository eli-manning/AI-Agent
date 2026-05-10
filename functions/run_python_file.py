from functions.validate_path import validate_path
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    target, error = validate_path(
        working_directory, file_path, check_is_file=True, running=True)
    if error:
        return error
    try:
        command = ["python", target]
        if args:
            command.extend(args)
        # timeout prevents hanging indefinitely on scripts with infinite loops
        # cwd ensures relative file operations inside the script resolve correctly
        subprocess_result = subprocess.run(
            command, capture_output=True, text=True, cwd=working_directory, timeout=30)
        output_parts = []

        if subprocess_result.returncode != 0:
            output_parts.append(
                f"Process exited with code {subprocess_result.returncode}")

        # always return something so the model knows the script ran but produced nothing
        if not subprocess_result.stdout and not subprocess_result.stderr:
            output_parts.append("No output produced")
        else:
            if subprocess_result.stdout:
                output_parts.append(f"STDOUT: {subprocess_result.stdout}")
            if subprocess_result.stderr:
                output_parts.append(f"STDERR: {subprocess_result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"

# schema tells the model what this function does and what arguments it accepts
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file at the specified path relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)
