import os
import shutil
from pathlib import Path

from backend.const import FIRST, DEFAULT_PLAYLIST_PATH


def make_dirs(playlist_path: str) -> None:
    path_dirs = [my_dir for my_dir in playlist_path.split('/') if my_dir]
    playlist_path = '/'.join(path_dirs)
    if playlist_path != DEFAULT_PLAYLIST_PATH:
        os.chdir(playlist_path)
    playlist_path = Path(playlist_path)
    playlist_path.mkdir(parents=True, exist_ok=True)


def remove_playlist(playlist_path: str, playlist_title: str) -> None:
    shutil.rmtree(path=f'{playlist_path}/{playlist_title}')


def remove_old_dirs(playlist_path: str) -> None:
    root_dir = [my_dir for my_dir in playlist_path.split('/') if my_dir][FIRST]
    shutil.rmtree(path=root_dir)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
