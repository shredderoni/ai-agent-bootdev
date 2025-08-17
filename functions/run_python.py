import os, subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python script located in the current working directory. "
        "Supports passing optional command-line arguments. "
        "The file path must be relative to the working directory, and execution "
        "is restricted to files within this directory (no external paths allowed)."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the Python file that should be executed. "
                    "Example: 'scripts/my_script.py'. The path must be within the current "
                    "working directory; absolute paths or paths referencing parent directories "
                    "(e.g., '../') are not permitted."
                ),
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Optional space-separated string of command-line arguments to pass "
                    "to the Python file when executed. "
                    "Example: '--mode test --verbose'. "
                    "If omitted or provided as an empty string, the Python file runs without arguments."
                ),
            ),
        },
        required=["filepath"],
    ),
)


def run_python_file(working_directory, filepath, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, filepath))
    full_path = os.path.join(working_directory, filepath)
    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'Error: Cannot execute "{filepath}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{filepath}" not found.'

        if not filepath.endswith(".py"):
            return f'Error: "{filepath}" is not a Python file.'

        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)

        completed_process = subprocess.run(
            commands, timeout=30, cwd=abs_working_dir, capture_output=True, text=True
        )
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
