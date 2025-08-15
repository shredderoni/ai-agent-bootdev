import os


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


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    MAX_CHARS = 10000

    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'\tError: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'\tError: File not found or is not a regular file: "{file_path}"'

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


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    try:
        if not os.path.realpath(full_path).startswith(
            os.path.realpath(working_directory)
        ):
            return f'\tError: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
