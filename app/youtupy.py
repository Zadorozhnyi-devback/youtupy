import sys
from typing import List

from const import WITHOUT_SCRIPT_NAME, PLAYLIST_URL, DESTINATION_PATH
from handlers.data_handlers import (
    get_playlist, get_dir_path, get_dir_mp4_files, convert_mp4_to_mp3, remove_videos,
)
from validators import validate_sys_args, validate_video_downloading


def main(sys_args: List[str]):
    # print('first', sys_args[DESTINATION_PATH])
    if validate_sys_args(sys_args=sys_args):
        playlist = get_playlist(playlist_url=sys_args[PLAYLIST_URL])
        # print('disss', sys_args[DESTINATION_PATH])
        dir_path = get_dir_path(
            playlist_title=playlist.title,
            path_to_playlists=sys_args[DESTINATION_PATH] if len(sys_args) > 1 else None
        )
        # print('DIRRR', dir_path)
        download_complete = validate_video_downloading(playlist=playlist, dir_path=dir_path)
        if download_complete:
            # print('success', download_complete)
            dir_videos = get_dir_mp4_files(dir_path=dir_path)
            # print('dir videos', dir_videos)
            # print('dir path', dir_path)
            convert_mp4_to_mp3(dir_videos=dir_videos, dir_path=dir_path)
            remove_videos(dir_videos=dir_videos, dir_path=dir_path)
        print('Success, bro)')
        # print('Thanks, now you can follow /youtupy1/')


if __name__ == "__main__":
    main(sys_args=sys.argv[WITHOUT_SCRIPT_NAME:])
