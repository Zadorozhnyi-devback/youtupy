import os
import shutil

from backend.const import FIRST


def make_dirs(dir_path: str, new_dir_path: str = '') -> None:
    dirs = [my_dir for my_dir in dir_path.split('/') if my_dir]
    for my_dir in dirs:
        new_dir_path += f'{my_dir}/'
        try:
            os.mkdir(new_dir_path)
        except FileExistsError:
            continue


def remove_old_dirs(dir_path: str) -> None:
    root_dir = [my_dir for my_dir in dir_path.split('/') if my_dir][FIRST]
    shutil.rmtree(path=root_dir)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
