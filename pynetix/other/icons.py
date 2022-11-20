from os import remove

from PyQt6.QtGui import QIcon

from pynetix import __resources__
from pynetix.other.colours import Colour


class Icon:

    icons = {'Arrow Down': 'down_arrow.svg'}

    @staticmethod
    def get_icon(name: str):
        directory = __resources__ / 'icons' / 'coloured'

        return QIcon(str(directory / Icon.icons[name]))

    @staticmethod
    def update_colours():
        directory = __resources__ / 'icons'

        for icon in Icon.icons.values():
            remove(directory / 'coloured' / icon)

            with open(directory / 'raw' / icon, 'r') as f:
                content = f.read()
            for colour in Colour:
                content = content.replace(fr'$({colour})', Colour[colour])
            with open(directory / 'coloured' / icon, 'w') as f:
                f.write(content)
