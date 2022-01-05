import os
from typing import List

from pytube import Playlist

from backend.handlers.validation_handlers import make_dirs, remove_old_dirs
from backend.const import DESTINATION_PATH, PLAYLIST_URL, DEFAULT_DIR_PATH


def validate_path_existing(dir_path: str) -> None:
    try:
        os.listdir(dir_path)
    except FileNotFoundError:
        make_dirs(dir_path=dir_path)
    except NotADirectoryError:
        remove_old_dirs(dir_path=dir_path)
        make_dirs(dir_path=dir_path)


def validate_playlist_existing(playlist_url) -> bool:
    print('url', playlist_url)
    playlist = Playlist(url=playlist_url)
    print('salal', playlist)
    if not playlist.videos:
        return False
    return True


# def validate_user_answer(dir_path: str):
#     while True:
#         user_answer = input('Decision: ')
#         # print(user_answer == 0)
#         if is_integer(value=user_answer) or not user_answer:
#             if not user_answer or int(user_answer) == 0:
#                 remove_old_dirs(dir_path=dir_path)
#                 make_dirs(dir_path=dir_path)
#                 break
#             if int(user_answer) == 1:
#                 sys.exit('See you next time :P')
#
#         print("Don't understand you")


def validate_playlist_loaded(args: List[str]) -> bool:
    playlist = Playlist(url=args[PLAYLIST_URL])
    dir_path = args[DESTINATION_PATH] if len(args) > 1 else DEFAULT_DIR_PATH
    try:
        dirs = os.listdir(path=dir_path)
    except FileNotFoundError:
        make_dirs(dir_path=dir_path)
        dirs = os.listdir(path=dir_path)
    if playlist.title in dirs:
        return False
    return True
#         validate_user_answer(dir_path=dir_path)


def validate_path_to_dir(dir_path: str) -> str:
    dir_path = dir_path[1:] if dir_path.startswith('/') else dir_path
    return dir_path


    # raise URLError(
    #     '''
    # Something went wrong. Got playlist but got error during downloading video
# '''
#     )
