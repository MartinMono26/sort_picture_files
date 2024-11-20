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
    with file_path.open('rb') as file:
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
        dir_path = Path(directory)
        for file_path in dir_path.rglob('*'):
            print(f'file_path {file_path} found')
            if file_path.is_file():
                print(f'adding its hash to existing_files_hashes {file_hash(file_path)}')
                existing_files_hashes.add(file_hash(file_path))

    # Iterate over files in target_directory and remove them if their hash exists in existing_files_hashes
    target_path = Path(target_directory)
    for file_path in target_path.rglob('*'):
        if file_path.is_file() and file_hash(file_path) in existing_files_hashes:
            print(f'Removing {file_path} as it is already sorted.')
            file_path.unlink()


if __name__ == '__main__':
    # Example usage
    TARGET_DIRECTORY = r'../workspace/VRAC'

    DIRECTORIES_TO_CHECK = [
        str(path) for path in Path(TARGET_DIRECTORY).parent.iterdir()
        if path.is_dir() and path != Path(TARGET_DIRECTORY)
    ]

    main(TARGET_DIRECTORY, DIRECTORIES_TO_CHECK)
