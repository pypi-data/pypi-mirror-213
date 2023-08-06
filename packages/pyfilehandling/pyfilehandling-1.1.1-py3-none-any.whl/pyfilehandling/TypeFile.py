def save_int(path: str,data: int,mode: str ="w") -> bool:

    """Writes data to a file.

    Args:

        path (str): The path of the file.

        data (str): The data to be written.

        mode (str, optional): The file opening mode. Defaults to "w" (write mode).

    Returns:

        bool: True if the write operation is successful, False otherwise.

    """

    with open(path, mode) as f:

        f.write(str(data))

        return True

def load_int(path: str) -> int:

    """Reads the contents of a file.

    Args:

        path (str): The path of the file.

    Returns:

        int: Integer stored in file.

    """

    with open(path, "r") as f:

        return int(f.read())

        

def save_list(path: str,data: list,mode: str='w') -> bool:

    """Writes data to a file.

    Args:

        path (str): The path of the file.

        data (str): The data to be written.

        mode (str, optional): The file opening mode. Defaults to "w" (write mode).

    Returns:

        bool: True if the write operation is successful, False otherwise.

    """

    with open(path,mode) as f:

        for entry in data:

            f.write(str(entry) + '\n')

        return True

def load_list(path: str) -> list:

    """Reads the contents of a file.

    and return a list of content

    Args:

        path (str): The path of the file.

    Returns:

        int: Integer stored in file.

    """

    data = []

    with open(path, "r") as f:

        for text in f.readlines():

            text = text[0:-1]

            if text == str(True) or text == str(False):

                if text == str(True):

                    data.append(True)

                else:

                    data.append(False)

            elif text.startswith('[') and text.endswith(']'):

               data.append(text)

            elif text.startswith('(') and text.endswith(')'):

                data.append(text)

            elif text.startswith('{') and text.endswith('}'):

                data.append(text)

            elif not text.isalpha():

                text = float(text)

                data.append(text)

            else:

                data.append(text)

    return data
