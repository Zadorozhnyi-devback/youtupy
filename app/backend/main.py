from typing import List

from backend.const import PLAYLIST_URL, DESTINATION_PATH
from backend.handlers.data_handlers import (
    get_playlist, get_dir_path, get_dir_mp4_files, convert_mp4_to_mp3, remove_videos
)
from backend.validators import validate_args, validate_video_downloading


def main(args: List[str]):
    if validate_args(args=args):
        # lock.acquire()
        playlist = get_playlist(playlist_url=args[PLAYLIST_URL])
        dir_path = get_dir_path(
            playlist_title=playlist.title,
            path_to_playlists=args[DESTINATION_PATH] if len(args) > 1 else None
        )
        download_complete = validate_video_downloading(playlist=playlist, output_path=dir_path)
        if download_complete:
            dir_videos = get_dir_mp4_files(dir_path=dir_path)
            convert_mp4_to_mp3(dir_videos=dir_videos, dir_path=dir_path)
            remove_videos(dir_videos=dir_videos, dir_path=dir_path)
        # lock.release()
        print('Success, bro)')
