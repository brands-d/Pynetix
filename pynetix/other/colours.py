import json

from pynetix import __resources__


class Colourscheme:
    # a class wrapper for a classmember dictionary acting itself
    # like a dictionary to simplify importing for other modules

    _colour = {}

    @staticmethod
    def update_colour_scheme(theme: str) -> None:
        try:
            with open(__resources__ / 'colourschemes' / f'{theme}.json') as f:
                Colourscheme._colour = json.load(f)
        except FileNotFoundError:
            print(
                f'Chosen theme "{theme}" does not exist. Fallback to "basic".')
            Colourscheme.update_colour_scheme('basic')

    def __delitem__(self, key: str) -> None:
        del Colourscheme._colour[key]

    def __getitem__(self, key: str) -> str:
        return Colourscheme._colour[key]

    def __setitem__(self, key: str, value: str) -> None:
        Colourscheme._colour.update({key: value})

    def __iter__(self):
        return Colour._colour.__iter__()

    def __next__(self):
        return Colour._colour.__next__()


Colour = Colourscheme()
