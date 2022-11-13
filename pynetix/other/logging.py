from datetime import datetime
from logging import Handler, Formatter

from pynetix.other.colours import Colour


class StatusBarHandler(Handler):

    def __init__(self, statusbar, *args) -> None:
        self.statusbar = statusbar
        super().__init__(*args)

    def emit(self, record) -> None:

        duration = record.args[0] if record.args else 0
        style, message = self.format(record)

        self.statusbar.setStyleSheet(style)
        self.statusbar.showMessage(message, duration)


class ColoredStatusBarFormatter(Formatter):

    def __init__(self) -> None:
        super().__init__()

    def format(self, record) -> None:
        time = datetime.now().strftime('%H:%M:%S')
        message = f'{time}    {record.msg}'

        if record.levelname == 'ERROR':
            style = f'color: {Colour["RED"]}; font-weight: bold'

        elif record.levelname == 'WARNING':
            style = f'color: {Colour["ORANGE"]}'

        else:
            style = f'color: {Colour["WHITE"]}'

        return style, message
