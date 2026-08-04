from .motor import screen
from .monitor import start
from os import remove
from os.path import isfile

if __name__ == "__main__":
    try:
        if isfile("logs.txt"):
            remove("logs.txt")
        visual = screen(150, start)
    except KeyboardInterrupt:
        print("\n\033[1;38;2;255mStopping program.\033[0m")
