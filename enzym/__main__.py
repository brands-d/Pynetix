from sys import exit
from signal import signal, SIGINT, SIG_DFL
from enzym.app import App


if __name__ == '__main__':
    signal(SIGINT, SIG_DFL)  # allows force quit with "ctrl+c"
    App().run()
