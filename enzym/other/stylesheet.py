from enzym import __resources__
from enzym.other.colours import Colour


class Style:

    @staticmethod
    def get_style(widget: str) -> str:
        with open(__resources__ / 'stylesheets' / f'{widget}.qss', 'r') as f:
            sheet = f.read()

        for colour in Colour:
            sheet = sheet.replace(fr'$({colour})', Colour[colour])

        return sheet
