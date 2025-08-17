import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    directory_list = ""
    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for {directory} directory:")

    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'\tError: "{directory}" is not a directory'

        for filename in os.listdir(full_path):
            files_path = os.path.join(full_path, filename)
            directory_list += f"- {filename}: file_size={os.path.getsize(files_path)}, is_dir={os.path.isdir(files_path)}\n"
        return directory_list

    except Exception as e:
        return f"Error: {e}"
