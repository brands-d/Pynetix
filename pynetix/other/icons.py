from os import remove, path, mkdir
from logging import getLogger

from PySide6.QtGui import QIcon

from pynetix import __resources__, __project__
from pynetix.other.colours import Colour


class Icon:

    icons = {'Arrow Down': 'down_arrow.svg',
             'Arrow Right': 'right_arrow.svg'}

    @staticmethod
    def getIcon(name: str):
        directory = __resources__ / 'icons' / 'coloured'
        iconPath = str(directory / Icon.icons[name])

        if path.isfile(iconPath):
            try:
                icon = QIcon(iconPath)
            except ValueError:
                getLogger(__project__).warning(f'Icon "{name}" not readable.')
                icon = QIcon()
        else:
            getLogger(__project__).warning(f'Icon "{name}" not found.')
            icon = QIcon()

        return icon

    @staticmethod
    def getIconPath(name: str) -> str:
        directory = __resources__ / 'icons' / 'coloured'
        iconPath = str(directory / Icon.icons[name])

        if path.isfile(iconPath):
            return iconPath
        else:
            getLogger(__project__).warning(f'Icon "{name}" not found.')
            return ''

    @staticmethod
    def updateColours():
        directoryColoured = __resources__ / 'icons' / 'coloured'
        directoryRaw = __resources__ / 'icons' / 'raw'

        if not path.isdir(directoryColoured):
            mkdir(directoryColoured)

        for icon in Icon.icons.values():
            try:
                remove(directoryColoured / icon)
            except FileNotFoundError:
                pass

            try:
                with open(directoryRaw / icon, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                getLogger(__project__).warning(f'Icon "{icon}" not found.')
            else:
                for colour in Colour:
                    content = content.replace(fr'$({colour})', Colour[colour])
                with open(directoryColoured / icon, 'w') as f:
                    f.write(content)
