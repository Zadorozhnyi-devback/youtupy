import subprocess
from pathlib import Path
from typing import List, Union
from urllib.error import URLError

from pytube import Playlist, YouTube

from backend.const import VID_NAME, RETRY_AMOUNT


def get_playlist(playlist_url: str) -> Playlist:
    return Playlist(url=playlist_url)


def get_path_to_playlist(playlist_title: str, playlist_path: str) -> str:
    path = f'{playlist_path}/{playlist_title}'
    return path


def get_dir_mp4_files(path_to_dir: str) -> List[Path]:
    videos = [file for file in Path(path_to_dir).glob('**/*.mp4')]
    return videos


def convert_mp4_to_mp3(videos: List[Path], destination_path: str) -> None:
    for video in videos:
        subprocess.call(
            [
                'ffmpeg', '-i', video,
                f"{destination_path}/{video.name.split('.mp4')[VID_NAME]}.mp3"

            ]
        )


def remove_videos(dir_videos: List[Path]) -> None:
    for video in dir_videos:
        video.unlink()


def download_playlist(
    playlist: Playlist, path_to_playlist: str
) -> None:
    for video in playlist.videos:
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=path_to_playlist, filename=f'{video.title}.mp4'
        )


def try_download(
    process_func: str, args: List[Union[Playlist, YouTube]]
) -> bool:
    for _ in range(RETRY_AMOUNT):
        try:
            # didn't find another solution, so call func by its name like this
            eval(f"{process_func}(*args)")
            return True
        except URLError:
            continue


def check_and_download_playlist(
    playlist: Playlist, path_to_playlist: str,
    selected_extension: str,
    process_func: str = 'download_playlist'
) -> None:
    download_complete = try_download(
        process_func=process_func,
        args=[playlist, path_to_playlist]
    )
    if download_complete and selected_extension == '.mp3':
        dir_videos = get_dir_mp4_files(path_to_dir=path_to_playlist)
        convert_mp4_to_mp3(
            videos=dir_videos, destination_path=path_to_playlist
        )
        remove_videos(dir_videos=dir_videos)


def download_video(video: YouTube, path: str) -> None:
    # сделать выпадашку с выбором качества видео
    video.streams.filter(
        file_extension='mp4',
    ).get_highest_resolution().download(
        output_path=path, filename=f'{video.title}.mp4'
    )


def check_and_download_video(
    video_url: str,
    selected_extension: str,
    destination_path: str,
    process_func: str = 'download_video'
) -> None:
    video = YouTube(url=video_url)
    download_complete = try_download(
        process_func=process_func, args=[video, destination_path]
    )
    if download_complete and selected_extension == '.mp3':
        video = [
            video for video
            in Path(destination_path).glob(f'**/{video.title}.mp4') if video
        ]
        convert_mp4_to_mp3(videos=video, destination_path=destination_path)
        remove_videos(dir_videos=video)
