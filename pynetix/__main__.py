from sys import exit
from signal import signal, SIGINT, SIG_DFL

from pynetix.app import App


if __name__ == '__main__':
    signal(SIGINT, SIG_DFL)  # allows force quit with "ctrl+c"
    exit(App().exec())
