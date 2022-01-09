import os
import shutil
from pathlib import Path

from backend.const import FIRST, DEFAULT_PLAYLIST_PATH


def chdir_if_path_not_default(playlist_path: Path) -> None:
    if playlist_path.name != DEFAULT_PLAYLIST_PATH:
        os.chdir(playlist_path)


def make_dirs(playlist_path: Path) -> None:
    path_dirs = [my_dir for my_dir in playlist_path.name.split('/') if my_dir]
    playlist_path = Path('/'.join(path_dirs))
    chdir_if_path_not_default(playlist_path=playlist_path)
    playlist_path.mkdir(parents=True, exist_ok=True)


def remove_playlist_dir(playlist_path: Path, playlist_title: str) -> None:
    shutil.rmtree(path=f'{playlist_path}/{playlist_title}')


def remove_old_dirs(playlist_path: Path) -> None:
    root_dir = [
        my_dir for my_dir in playlist_path.name.split('/') if my_dir
    ][FIRST]
    shutil.rmtree(path=root_dir)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
