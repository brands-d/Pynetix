from logging import getLogger
from re import search

from numpy import array, nan
from openpyxl import load_workbook

from pynetix import __project__
from pynetix.models.reaction import Reaction


class Plate:
    _md = {'User': {'loc': 'A3', 'name': 'User'},
           'Path': {'loc': 'A4', 'name': 'Path'},
           'Test ID': {'loc': 'A5', 'name': 'Test ID'},
           'Test Name': {'loc': 'A6', 'name': 'Test Name'},
           'Date': {'loc': 'A7', 'name': 'Date'},
           'Time': {'loc': 'A8', 'name': 'Time'},
           'ID1': {'loc': 'A9', 'name': 'ID1'},
           'ID2': {'loc': 'A10', 'name': 'ID2'},
           'ID3': {'loc': 'A11', 'name': 'ID3'}}

    def __init__(self, file, dimensions=(8, 12)) -> None:

        self.metaData = {}
        self.filePath = str(file)
        self.dimensions = dimensions
        self.reactions = None
        self.times = None
        self.timeUnits = None
        self.results = None

        self._parseFile()

    @property
    def timeLabel(self):
        return f'Time t / {self.timeUnits}'

    def changeMetaData(self, metaData: str, value: str) -> None:
        try:
            wb, ws = self._openWorkbook()
        except:
            getLogger(__project__).error(
                f'Changing meta data failed. File not accessible anymore.', 20)

        if metaData == 'Time':
            pass
        elif metaData == 'Date':
            pass

        ws[Plate._md[metaData]['loc']
           ].value = f"{Plate._md[metaData]['name']}: {value}"
        wb.save(self.filePath)
        getLogger(__project__).info(
            f"Changed '{metaData}' to '{value}' successfully.")

    def _openWorkbook(self):
        try:
            wb = load_workbook(self.filePath)
            ws = wb.active
            return wb, ws
        except:
            raise ValueError

    def _parseFile(self) -> None:
        _, ws = self._openWorkbook()
        version = self._checkFileVersion(ws)
        self.metaData = self._parseMetaData(ws, version=version)
        valueUnits = self._parseValueUnits(ws, version=version)
        self.times = self._parseTime(ws, version=version)
        self._parseReactions(ws, valueUnits, version=version)

    def _checkFileVersion(self, ws) -> str:
        if ws['A10'].value is None:
            return 'new'
        else:
            return 'old'

    def _parseMetaData(self, ws, version='old') -> None:
        metaData = {}
        for md, info in Plate._md.items():

            if version == 'new' and md[:2] == 'ID':
                continue

            raw = ws[info['loc']].value
            reg = fr"^{info['name']}: (.*)$"
            result = search(reg, raw)
            groups = result.groups() if result is not None else ['', ]
            value = groups[0]

            metaData.update({md: value})

        return metaData

    def _parseValueUnits(self, ws, version='old') -> str:
        loc = 'D12' if version == 'old' else 'D9'
        return search(r'as (.*)$', ws[loc].value).groups()[0]

    def _parseTime(self, ws, version='old'):
        reg = r'Cycle \d* \((.* h)? ?(.* min)? ?(.* s)?\)'
        i = 16 if version == 'old' else 13
        delta = 4 + self.dimensions[0]
        times = []

        while True:
            if ws[f'A{i:d}'].value:
                h, m, s = search(reg, ws[f'A{i:d}'].value).groups()
                m = int(search('(\d*)', m).groups()[0])
                s = 0 if s is None else int(search('(\d*)', s).groups()[0])
                if h is not None:
                    h = int(search('\d*', h).groups()[0])
                    self.timeUnits = 'h'
                else:
                    h = 0
                    self.timeUnits = 's'

                times.append(24*60*h+60*m+s)
                i += delta
            else:
                break

        return array(times)

    def _parseReactions(self, ws, units: str, version='old') -> None:
        start_row = 19 if version == 'old' else 16
        start_col = 2
        delta = 4 + self.dimensions[0]
        self.reactions = []

        for row in range(self.dimensions[0]):
            self.reactions.append([])
            for col in range(self.dimensions[1]):
                cycle = 0
                values = []
                while True:
                    value = ws.cell(start_row+row+cycle, start_col+col).value
                    if value:
                        if value in ['overflow']:
                            value = nan
                        values.append(value)
                        cycle += delta
                    else:
                        break
                self.reactions[row].append(
                    Reaction(self, values, row, col, units))
