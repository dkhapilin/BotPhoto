import pathlib


def check_and_create_directory(path: pathlib.Path):

    path.mkdir(parents=True, exist_ok=True)

