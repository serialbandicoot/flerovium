import os


def strip(value: str):
    if value is not None:
        return value.strip()


def image_path():
    return os.path.join(database_path(), "images")


def database_path():
    return os.path.join("/Users/sam.treweek/Desktop/fl_data")