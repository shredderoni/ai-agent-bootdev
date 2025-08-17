import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file the specified content or create the file if it doesn't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
