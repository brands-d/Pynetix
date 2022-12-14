from datetime import datetime
from logging import Handler, Formatter

from pynetix.resources.resources import Resource


class StatusBarHandler(Handler):

    def __init__(self, statusbar, *args) -> None:
        self.statusbar = statusbar
        self.lastMessage = {'level': 'INFO'}

        super().__init__(*args)

    def emit(self, record) -> None:

        lastLevel = self.lastMessage['level']
        level = record.levelname
        passMessage = False
        if level == 'ERROR':
            passMessage = True
        elif level == 'WARNING' and lastLevel != 'ERROR':
            passMessage = True
        elif level == 'INFO' and lastLevel == 'INFO':
            passMessage = True

        if not passMessage:
            # check if long enough ago
            timePassed = (datetime.now() -
                          self.lastMessage['time']).total_seconds()
            if timePassed > self.lastMessage['duration']:
                passMessage = True

        if passMessage:
            duration = record.args[0] if record.args else 0
            style, message = self.format(record)

            self.statusbar.setStyleSheet(style)
            self.statusbar.showMessage(message)
            self.lastMessage.update(
                {'message': message, 'duration': duration, 'level': record.levelname,
                 'time': datetime.now()})


class ColoredStatusBarFormatter(Formatter):

    def __init__(self) -> None:
        super().__init__()

    def format(self, record) -> None:
        time = datetime.now().strftime('%H:%M:%S')
        message = f'{time}    {record.msg}'

        if record.levelname == 'ERROR':
            style = f'color: {Resource.theme["RED"]}; font-weight: bold'

        elif record.levelname == 'WARNING':
            style = f'color: {Resource.theme["ORANGE"]}'

        else:
            style = f'color: {Resource.theme["WHITE"]}'

        return style, message
