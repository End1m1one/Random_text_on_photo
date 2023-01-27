import os
from config import path


def deliting():
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


if __name__ == "__main__":
    deliting()
