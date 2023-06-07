import os

def ensure_directory_exists(path):
    """
    ensure_directory_exists Ensures that the given directory exists.

    It creates the directory if it doesn't exist. That's it.
    """     
    dirname = os.path.dirname(path)
    exists = os.path.exists(dirname)
    if not exists:
        os.makedirs(dirname)

