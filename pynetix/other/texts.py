from pathlib import Path

from pynetix import __resources__, __project_path__


class Texts:

    paths = {'about': 'about.html'}

    def get(self, file: str, **replacements) -> str:
        text = self._getText(file)
        if replacements:
            text = text.format(**replacements)

        return text

    def _getText(self, file: str) -> str:
        path = __project_path__ / 'pynetix' / \
            'resources' / 'texts' / Texts.paths[file]
        print(path)
        try:
            with open(path, 'r') as f:
                text = f.read()
        except:
            raise ValueError

        return text


Text = Texts()
