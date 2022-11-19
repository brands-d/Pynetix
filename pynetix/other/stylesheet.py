from os.path import exists

from pynetix import __resources__
from pynetix.other.colours import Colour


class Style:

    @staticmethod
    def get_style(widget: str) -> str:
        directory = __resources__ / 'stylesheets'
        user_file = directory / f'{widget}_user.qss'
        default_file = directory / f'{widget}.qss'

        if exists(user_file):
            with open(user_file, 'r') as f:
                sheet = f.read()
        else:
            with open(default_file, 'r') as f:
                sheet = f.read()

        for colour in Colour:
            sheet = sheet.replace(fr'$({colour})', Colour[colour])

        return sheet
