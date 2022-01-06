import os
import shutil
from pathlib import Path

from backend.const import FIRST


def make_dirs(dir_path: str) -> None:
    dirs = [my_dir for my_dir in dir_path.split('/') if my_dir]
    destination_path = '/'.join(dirs)
    os.chdir(destination_path)
    new_dir_path = Path(destination_path)
    new_dir_path.mkdir(parents=True, exist_ok=True)


def remove_old_dirs(dir_path: str) -> None:
    root_dir = [my_dir for my_dir in dir_path.split('/') if my_dir][FIRST]
    shutil.rmtree(path=root_dir)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
