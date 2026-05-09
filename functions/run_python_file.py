from functions.validate_path import validate_path
import subprocess


def run_python_file(working_directory, file_path, args=None):
    target, error = validate_path(
        working_directory, file_path, check_is_file=True, running=True)
    if error:
        return error
    try:
        command = ["python", target]
        if args:
            command.extend(args)
        subprocess_result = subprocess.run(
            command, capture_output=True, text=True, cwd=working_directory, timeout=30)
        output_parts = []

        # 1. Check return code first
        if subprocess_result.returncode != 0:
            output_parts.append(
                f"Process exited with code {subprocess_result.returncode}")

        # 2. Check for "No output produced"
        if not subprocess_result.stdout and not subprocess_result.stderr:
            output_parts.append("No output produced")
        else:
            # 3. Otherwise, add STDOUT and STDERR (if they have content)
            if subprocess_result.stdout:
                output_parts.append(f"STDOUT: {subprocess_result.stdout}")
            if subprocess_result.stderr:
                output_parts.append(f"STDERR: {subprocess_result.stderr}")

        # Join everything with newlines
        return "\n".join(output_parts)
    
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
