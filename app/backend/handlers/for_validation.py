import shutil
import os


def remove_file(path: str) -> None:
    os.remove(path=path)


def remove_dir(path: str) -> None:
    shutil.rmtree(path=path)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
