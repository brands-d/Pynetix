from datetime import datetime
from logging import Handler, Formatter

from pynetix.other.colours import Colour


class StatusBarHandler(Handler):

    def __init__(self, statusbar, *args) -> None:
        self.statusbar = statusbar
        self.last_message = {'level': 'INFO'}

        super().__init__(*args)

    def emit(self, record) -> None:

        last_level = self.last_message['level']
        level = record.levelname
        pass_message = False
        if level == 'ERROR':
            pass_message = True
        elif level == 'WARNING' and last_level != 'ERROR':
            pass_message = True
        elif level == 'INFO' and last_level == 'INFO':
            pass_message = True

        if not pass_message:
            # check if long enough ago
            time_passed = (datetime.now() -
                           self.last_message['time']).total_seconds()
            if time_passed > self.last_message['duration']:
                pass_message = True

        if pass_message:
            duration = record.args[0] if record.args else 0
            style, message = self.format(record)

            self.statusbar.setStyleSheet(style)
            self.statusbar.showMessage(message)
            self.last_message.update(
                {'message': message, 'duration': duration, 'level': record.levelname,
                 'time': datetime.now()})


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
