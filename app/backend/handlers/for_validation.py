import shutil
import os


__all__ = (
    'remove_file',
    'remove_dir'
)


def remove_file(path: str) -> None:
    os.remove(path=path)


def remove_dir(path: str) -> None:
    shutil.rmtree(path=path)
