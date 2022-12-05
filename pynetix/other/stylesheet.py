from os.path import exists

from pynetix import __resources__
from pynetix.other.colours import Colour


class Style:
    styles = {'Application': 'application',
              'SideBar': 'sidebar',
              'QSplitter Base': 'splitter_base',
              'QSplitter Hover': 'splitter_hover'}

    @staticmethod
    def getStyle(name: str) -> str:
        directory = __resources__ / 'stylesheets'
        userFile = directory / f'{Style.styles[name]}_user.qss'
        defaultFile = directory / f'{Style.styles[name]}.qss'

        if exists(userFile):
            with open(userFile, 'r') as f:
                sheet = f.read()
        else:
            with open(defaultFile, 'r') as f:
                sheet = f.read()

        for colour in Colour:
            sheet = sheet.replace(fr'$({colour})', Colour[colour])

        return sheet
