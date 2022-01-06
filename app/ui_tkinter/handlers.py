from time import sleep


def _progressbar_process(playlist_length: int) -> None:
    needed_time = playlist_length * 15 + 30
    sleep(needed_time)
