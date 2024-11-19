import os
import shutil
import random
from pathlib import Path


def create_directory_with_files(directory: Path, num_files: int, file_extension: str, forbidden_files_names_list=None):
    if forbidden_files_names_list is None:
        new_forbidden_files_names_list = []
    else:
        new_forbidden_files_names_list=forbidden_files_names_list

    if not directory.exists():
        directory.mkdir(parents=True)

    i = 1
    nb_created_files = 0
    while nb_created_files < num_files:
        file_name = f'file_{i:02d}{file_extension}'
        if file_name not in new_forbidden_files_names_list:
            file_path = directory / file_name
            file_path.touch()
            new_forbidden_files_names_list.append(file_name)
            nb_created_files += 1
        i += 1
    return new_forbidden_files_names_list


def duplicate_files_to_directory(source_dir: Path, target_dir: Path, fraction: float):
    source_files = list(source_dir.glob('*.png'))
    num_files_to_duplicate = int(len(source_files) * fraction)
    duplicate_files = random.sample(source_files, num_files_to_duplicate)

    if not target_dir.exists():
        target_dir.mkdir(parents=True)

    duplicated_files_list = set()
    for file in duplicate_files:
        shutil.copy(file, target_dir / file.name)
        duplicated_files_list.add(file.name)

    return duplicated_files_list


def generate_dirs_and_files(base_dir: Path):
    base_path = base_dir if base_dir else Path.cwd()
    vrac_dir = base_path / 'VRAC'
    d1_dir = base_path / 'd1'
    d2_dir = base_path / 'd2'

    # Create VRAC directory with 10 .png files
    vrac_files = create_directory_with_files(vrac_dir, 10, '.png')

    # Create d1 and d2 directories each with 10 .png files, with 50% duplicates from VRAC
    d1_duplicates = duplicate_files_to_directory(vrac_dir, d1_dir, 0.5)
    d2_duplicates = duplicate_files_to_directory(vrac_dir, d2_dir, 0.5)

    # Fill d1 and d2 with additional unique files to total 10 files each
    forbidden_files = create_directory_with_files(d1_dir, 10 - len(os.listdir(d1_dir)), '.png', vrac_files)
    forbidden_files = create_directory_with_files(d2_dir, 10 - len(os.listdir(d2_dir)), '.png', forbidden_files)


if __name__ == '__main__':
    workspace_dir = Path.cwd().parent / "workspace"
    generate_dirs_and_files(workspace_dir)
