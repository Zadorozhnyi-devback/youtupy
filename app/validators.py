import os
import sys
from typing import List
from urllib.error import URLError

from pytube import Playlist

from const import DESTINATION_PATH, PLAYLIST_URL, DEFAULT_DIR_PATH
from handlers.data_handlers import download_playlist_videos
from handlers.validation_handlers import make_dirs, remove_old_dirs, is_integer


def validate_no_sys_args(sys_args: List[str]) -> None:
    if not sys_args:
        raise ValueError(
            """
    You didn't pass the argument :(

    Please, pass the playlist url as in example below

    Example:
        python3 youtupy1.py https://some/test/youtube/music/playlist/url/
            """
        )


def validate_more_then_two_sys_arg(sys_args: List[str]) -> None:
    if len(sys_args) > 2:
        raise ValueError(
            '''
    Too much arguments
    
    First arg should be playlist url and second is optional path to destination folder
    
    Please, remove excess arguments'''
        )


def validate_path_existing(dir_path: str) -> None:
    try:
        os.listdir(dir_path)
    except FileNotFoundError:
        make_dirs(dir_path=dir_path)
    except NotADirectoryError:
        remove_old_dirs(dir_path=dir_path)
        make_dirs(dir_path=dir_path)


def validate_playlist_existing(playlist_url) -> None:
    playlist = Playlist(url=playlist_url)
    if not playlist.videos:
        raise ValueError(
            '''
    Something went wrong. There is empty playlist, check the url
            '''
        )


def validate_user_answer(dir_path: str):
    while True:
        user_answer = input('Decision: ')
        # print(user_answer == 0)
        if is_integer(value=user_answer) or not user_answer:
            if not user_answer or int(user_answer) == 0:
                remove_old_dirs(dir_path=dir_path)
                make_dirs(dir_path=dir_path)
                break
            if int(user_answer) == 1:
                sys.exit('See you next time :P')

        print("Don't understand you")


def validate_playlist_loaded(sys_args: List[str]) -> None:
    # print('sosooso')
    playlist = Playlist(url=sys_args[PLAYLIST_URL])
    dir_path = sys_args[DESTINATION_PATH] if len(sys_args) > 1 else DEFAULT_DIR_PATH
    # print('*' * 10, dir_path)
    try:
        dirs = os.listdir(path=dir_path)
    except FileNotFoundError:
        make_dirs(dir_path=dir_path)
        dirs = os.listdir(path=dir_path)
    if playlist.title in dirs:
        print(
            '''
    This playlist folder name already exists
    
    Leave empty and press 'enter' or pass 0 to rebuild or pass 1 to exit Youtupy
'''
        )
        validate_user_answer(dir_path=dir_path)


def validate_path_to_dir(dir_path: str) -> str:
    # print(dir_path)
    dir_path = dir_path[1:] if dir_path.startswith('/') else dir_path
    return dir_path


def validate_video_downloading(playlist: Playlist, dir_path: str, downloaded: bool = False) -> bool:
    for digit in range(3):
        try:
            download_playlist_videos(playlist=playlist, dir_path=dir_path)
            return True
        except URLError:
            continue
    raise URLError(
        '''
    Something went wrong. Got playlist but got error during downloading video
'''
    )


def validate_sys_args(sys_args: List[str]) -> bool:
    validate_no_sys_args(sys_args=sys_args)
    validate_more_then_two_sys_arg(sys_args=sys_args)
    if len(sys_args) > 1:
        # print('des', sys_args[DESTINATION_PATH])
        validate_path_existing(dir_path=sys_args[DESTINATION_PATH])
        sys_args[DESTINATION_PATH] = validate_path_to_dir(dir_path=sys_args[DESTINATION_PATH])
    validate_playlist_existing(playlist_url=sys_args[PLAYLIST_URL])
    validate_playlist_loaded(sys_args=sys_args)
    return True
