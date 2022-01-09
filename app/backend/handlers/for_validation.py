import shutil


def remove_dir(path: str) -> None:
    shutil.rmtree(path=path)


# def is_integer(value: Union[str, int]):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False
