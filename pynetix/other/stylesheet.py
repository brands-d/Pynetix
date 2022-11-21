from os.path import exists

from pynetix import __resources__
from pynetix.other.colours import Colour


class Style:
    styles = {'Application': 'application',
              'SideBar': 'sidebar',
              'QSplitter Base': 'splitter_base',
              'QSplitter Hover': 'splitter_hover'}

    @staticmethod
    def get_style(name: str) -> str:
        directory = __resources__ / 'stylesheets'
        user_file = directory / f'{Style.styles[name]}_user.qss'
        default_file = directory / f'{Style.styles[name]}.qss'

        if exists(user_file):
            with open(user_file, 'r') as f:
                sheet = f.read()
        else:
            with open(default_file, 'r') as f:
                sheet = f.read()

        for colour in Colour:
            sheet = sheet.replace(fr'$({colour})', Colour[colour])

        return sheet
