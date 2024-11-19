import os
import hashlib
from pathlib import Path
from typing import List


def file_hash(file_path: Path) -> str:
    """
    Generate SHA-256 hash of the file.

    Args:
    file_path (Path): The path to the file for which to generate the hash.

    Returns:
    str: The SHA-256 hash of the file as a hexadecimal string.
    """
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()


def main(target_directory: str, directories_to_check: List[str]) -> None:
    """
    Remove files from target_directory if they exist in any of directories_to_check.

    Args:
    target_directory (str): The directory from which files will be removed if they exist in directories_to_check.
    directories_to_check (List[str]): A list of directories to check for already sorted files.
    """
    # Create a set to store hashes of files in directories_to_check
    existing_files_hashes = set()

    for directory in directories_to_check:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                existing_files_hashes.add(file_hash(file_path))

    # Iterate over files in target_directory and remove them if their hash exists in existing_files_hashes
    for root, _, files in os.walk(target_directory):
        for file in files:
            file_path = Path(root) / file
            if file_hash(file_path) in existing_files_hashes:
                print(f'Removing {file_path} as it is already sorted.')
                os.remove(file_path)


if __name__ == '__main__':
    # Example usage
    TARGET_DIRECTORY = r'path\to\target\directory'
    DIRECTORIES_TO_CHECK = [
        r'path\to\directory1',
        r'path\to\directory2',
        # Add more directories as needed
    ]

    main(TARGET_DIRECTORY, DIRECTORIES_TO_CHECK)
