from os import remove, path, mkdir
from logging import getLogger

from PySide6.QtGui import QIcon

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
                getLogger(__project__).warning(f'Icon "{name}" not readable.')
                icon = QIcon()
        else:
            getLogger(__project__).warning(f'Icon "{name}" not found.')
            icon = QIcon()

        return icon

    @staticmethod
    def update_colours():
        directory_coloured = __resources__ / 'icons' / 'coloured'
        directory_raw = __resources__ / 'icons' / 'raw'

        if not path.isdir(directory_coloured):
            mkdir(directory_coloured)

        for icon in Icon.icons.values():
            try:
                remove(directory_coloured / icon)
            except FileNotFoundError:
                pass

            try:
                with open(directory_raw / icon, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                getLogger(__project__).warning(f'Icon "{icon}" not found.')
            else:
                for colour in Colour:
                    content = content.replace(fr'$({colour})', Colour[colour])
                with open(directory_coloured / icon, 'w') as f:
                    f.write(content)
