from datetime import datetime
from logging import Handler, Formatter


class StatusBarHandler(Handler):

    def __init__(self, statusbar, *args) -> None:
        self.statusbar = statusbar
        super().__init__(*args)

    def emit(self, record):

        style, message = self.format(record)
        self.statusbar.setStyleSheet(style)
        self.statusbar.showMessage(message)


class ColoredStatusBarFormatter(Formatter):

    def __init__(self, colour):

        self.colour = colour
        super().__init__()

    def format(self, record):

        time = datetime.now().strftime('%H:%M:%S')
        message = f'{time}    {record.msg}'

        if record.levelname == 'ERROR':
            style = f'color: {self.colour.RED.value}; font-weight: bold'

        elif record.levelname == 'WARNING':
            style = f'color: {self.colour.ORANGE.value}'

        else:
            style = f'color: {self.colour.WHITE.value}'

        return style, message
