import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the contents of, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    MAX_CHARS = 10000

    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > 10000:
                return (
                    file_content_string
                    + f'\n[...File "{file_path}" truncated at 10000 characters]'
                )
            else:
                return file_content_string

    except Exception as e:
        return f"Error: {e}"
