from os import remove, path
from logging import getLogger

from PyQt6.QtGui import QIcon

from pynetix import __resources__, __project__
from pynetix.other.colours import Colour


class Icon:

    icons = {'Arrow Down': 'down_arrow.svg',
             'Arrow Right': 'right_arrow.svg'}

    @staticmethod
    def get_icon(name: str):
        directory = __resources__ / 'icons' / 'coloured'
        icon_path = str(directory / Icon.icons[name])

        if path.isfile(icon_path):
            try:
                icon = QIcon(icon_path)
            except ValueError:
                getLogger(__project__).warning(f'Icon "{name}" not readable.', 5)
                icon = QIcon()
        else:
            getLogger(__project__).warning(f'Icon "{name}" not found.', 5)
            icon = QIcon()

        return icon

    @staticmethod
    def update_colours():
        directory = __resources__ / 'icons'

        for icon in Icon.icons.values():
            try:
                remove(directory / 'coloured' / icon)
            except FileNotFoundError:
                pass

            try:
                with open(directory / 'raw' / icon, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                getLogger(__project__).warning(f'Icon "{icon}" not found.', 5)
            else:
                for colour in Colour:
                    content = content.replace(fr'$({colour})', Colour[colour])
                with open(directory / 'coloured' / icon, 'w') as f:
                    f.write(content)
