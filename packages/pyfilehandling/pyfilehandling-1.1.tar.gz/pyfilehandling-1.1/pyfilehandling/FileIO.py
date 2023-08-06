import os

def create(path: str) -> None:

    """Creates a directory

    

    Args:

        path (str): The path of Directory

    """

    try:

        open(path,'x')

    except FileExistsError as _:

        print(f"FileAlreadyExist: \"{path}\" already exists")

def create_directory(path: str) -> None:

    """Creates a directory

    

    Args:

        path (str): The path of Directory

    """

    try:

        os.mkdir(path)

    except FileExistsError as _:

        print(f"DirectoryAlreadyExist: \"{path}\" already exists")

def write(path: str, data: str, mode="w") -> bool:

    """Writes data to a file.

    Args:

        path (str): The path of the file.

        data (str): The data to be written.

        mode (str, optional): The file opening mode. Defaults to "w" (write mode).

    Returns:

        bool: True if the write operation is successful, False otherwise.

    """

    with open(path, mode) as f:

        f.write(data)

        return True

def writeline(path: str, data: str, mode="w", end='\n', start="") -> bool:

    """Writes data to a file in a new line.

    Args:

        path (str): The path of the file.

        data (str): The data to be written.

        mode (str, optional): The file opening mode. Defaults to "w" (write mode).

        end (str, optional): The line ending character. Defaults to '\n' (newline).

        start (str, optional): The starting character(s) of each line. Defaults to "".

    Returns:

        bool: True if the write operation is successful, False otherwise.

    """

    with open(path, mode) as f:

        f.write(start + data + end)

        return True

def writelines(path: str, data: list, mode="w", end="\n", start="") -> bool:

    """Writes a list of data to a file, each in a new line.

    Args:

        path (str): The path of the file.

        data (list): The list of data to be written.

        mode (str, optional): The file opening mode. Defaults to "w" (write mode).

        end (str, optional): The line ending character. Defaults to '\n' (newline).

        start (str, optional): The starting character(s) of each line. Defaults to "".

    Returns:

        bool: True if the write operation is successful, False otherwise.

    """

    with open(path, mode) as f:

        for item in data:

            f.write(start + str(item) + end)

        return True

def read(path: str) -> str:

    """Reads the contents of a file.

    Args:

        path (str): The path of the file.

    Returns:

        str: The contents of the file.

    """

    with open(path, "r") as f:

        return f.read()

def readline(path: str) -> str:

    """Reads a single line from a file.

    Args:

        path (str): The path of the file.

    Returns:

        str: The first line of the file.

    """

    with open(path, "r") as f:

        return f.readline().split()[0]

def readlines(path: str) -> list:

    """Reads all lines from a file and returns them as a list.

    Args:

        path (str): The path of the file.

    Returns:

        list: A list of lines from the file.

    """

    lines = []

    with open(path, 'r') as f:

        for line in f.readlines():

            lines.append(line.split()[0])

    return lines
