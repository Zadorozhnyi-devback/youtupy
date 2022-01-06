import os
from typing import List

from pytube import Playlist

from backend.handlers.for_validation import (
    make_dirs, remove_old_dirs, chdir_if_path_not_default
)
from backend.const import PLAYLIST_PATH, PLAYLIST_URL, DEFAULT_PLAYLIST_PATH


def validate_path_existing(playlist_path: str) -> None:
    try:
        chdir_if_path_not_default(playlist_path=playlist_path)
        os.listdir(playlist_path)
    except FileNotFoundError:
        make_dirs(playlist_path=playlist_path)
    except NotADirectoryError:
        remove_old_dirs(playlist_path=playlist_path)
        make_dirs(playlist_path=playlist_path)


def validate_playlist_existing(playlist_url) -> bool:
    playlist = Playlist(url=playlist_url)
    if not playlist.videos:
        return False
    return True


# def validate_user_answer(playlist_path: str):
#     while True:
#         user_answer = input('Decision: ')
#         # print(user_answer == 0)
#         if is_integer(value=user_answer) or not user_answer:
#             if not user_answer or int(user_answer) == 0:
#                 remove_old_dirs(playlist_path=playlist_path)
#                 make_dirs(playlist_path=playlist_path)
#                 break
#             if int(user_answer) == 1:
#                 sys.exit('See you next time :P')
#
#         print("Don't understand you")


def get_listdir(playlist_path: str) -> List[str]:
    chdir_if_path_not_default(playlist_path=playlist_path)
    dirs = os.listdir(path=playlist_path)
    return dirs


def validate_playlist_loaded(args: List[str]) -> bool:
    playlist = Playlist(url=args[PLAYLIST_URL])
    playlist_path = (
        args[PLAYLIST_PATH] if len(args) > 1 else DEFAULT_PLAYLIST_PATH
    )
    try:
        dirs = get_listdir(playlist_path=playlist_path)
    except FileNotFoundError:
        make_dirs(playlist_path=playlist_path)
        dirs = get_listdir(playlist_path=playlist_path)
    if playlist.title in dirs:
        return False
    return True
#         validate_user_answer(playlist_path=playlist_path)
