from json import load
from logging import getLogger
from os import listdir, mkdir, path, remove
from os.path import exists
from pathlib import Path

from PySide6.QtGui import QIcon

from pynetix import (__date__, __description__, __project__, __resources__,
                     __version__)


class Resource:

    stylesheetsDir = __resources__ / 'stylesheets'
    styles = {'Application': 'application',
              'SideBar': 'sidebar',
              'QSplitter Base': 'splitter_base',
              'QSplitter Hover': 'splitter_hover'}

    themeDir = __resources__ / 'colourschemes'
    theme = {'WHITE': '#ffffff', 'RED': '#ff0000', 'ORANGE': '#fe8019', }

    iconDir = __resources__ / 'icons'
    iconRawDir = iconDir / 'raw'
    iconColouredDir = iconDir / 'coloured'
    icons = {'Arrow Down': 'down_arrow.svg',
             'Arrow Right': 'right_arrow.svg'}

    textDir = __resources__ / 'texts'
    texts = {'about': 'about.html'}
    replacements = {'description': __description__, 'version': __version__,
                    'date': __date__}

    @staticmethod
    def getStyle(name: str) -> str:
        userFile = Resource.stylesheetsDir / \
            f'{Resource.styles[name]}_user.qss'
        defaultFile = Resource.stylesheetsDir / f'{Resource.styles[name]}.qss'

        try:
            sheet = Resource._readFile(userFile)
        except FileNotFoundError:
            sheet = Resource._readFile(defaultFile)

        sheet = Resource._applyTheme(sheet)

        return sheet

    @staticmethod
    def updateColourScheme(theme: str) -> None:
        file = Resource.themeDir / f'{theme}.json'
        try:
            with open(file) as f:
                Resource.theme = load(f)
            Resource._updateIconColours()
        except:
            raise ValueError

    @staticmethod
    def getColour(colour: str) -> str:
        return Resource.theme[colour]

    @staticmethod
    def listThemes():
        availableThemes = []
        for file in listdir(str(Resource.themeDir)):
            try:
                with open(Resource.themeDir / file, 'r') as f:
                    load(f)
            except:
                pass
            else:
                availableThemes.append(Path(file).stem)

        return tuple(availableThemes)

    @staticmethod
    def getIcon(name: str):
        iconPath = str(Resource.iconColouredDir / Resource.icons[name])

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
        iconPath = str(Resource.iconColouredDir / Resource.icons[name])

        if path.isfile(iconPath):
            return iconPath
        else:
            #getLogger(__project__).warning(f'Icon "{name}" not found.')
            return ''

    @staticmethod
    def getText(text: str) -> str:
        path = Resource.textDir / Resource.texts[text]
        text = Resource._readFile(path).format(**Resource.replacements)

        return text

    @staticmethod
    def _applyTheme(sheet: str) -> str:
        for colour in Resource.theme:
            sheet = sheet.replace(fr'$({colour})', Resource.theme[colour])

        return sheet

    @staticmethod
    def _readFile(path):
        if exists(path):
            with open(path, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError

    @staticmethod
    def _updateIconColours():
        if not path.isdir(Resource.iconColouredDir):
            mkdir(Resource.iconColouredDir)

        for icon in Resource.icons.values():
            try:
                remove(Resource.iconColouredDir / icon)
            except FileNotFoundError:
                pass

            try:
                with open(Resource.iconRawDir / icon, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                pass
                getLogger(__project__).warning(f'Icon "{icon}" not found.')
            else:
                content = Resource._applyTheme(content)
                with open(Resource.iconColouredDir / icon, 'w') as f:
                    f.write(content)
