from datetime import date, time
from re import search

from numpy import array
from openpyxl import load_workbook

from pynetix.models.reaction import Reaction


class Plate:
    _md = {'User': {'loc': 'A3', 'reg': r'^User: (.*)$'},
           'Path': {'loc': 'A4', 'reg': r'^Path: (.*)$'},
           'Test ID': {'loc': 'A5', 'reg': r'^Test ID: (.*)$'},
           'Test Name': {'loc': 'A6', 'reg': r'^Test Name: (.*)$'},
           'Date': {'loc': 'A7', 'reg': r'^Date: (\d{1,2})/(\d{1,2})/(\d{4})$'},
           'Time': {'loc': 'A8', 'reg': r'^Time: (\d{1,2}):(\d{1,2}):(\d{1,2}) ([A-Z]{2})$'},
           'ID1': {'loc': 'A9', 'reg': r'^ID1: (.*)$'},
           'ID2': {'loc': 'A10', 'reg': r'^ID2: (.*)$'},
           'ID3': {'loc': 'A11', 'reg': r'^ID3: (.*)$'}}

    def __init__(self, file, dimensions=(8, 12)) -> None:

        self.metaData = {}
        self.dimensions = dimensions
        self.reactions = None
        self.time = None
        self.timeUnits = None
        self.results = None

        self._parseFile(file)

    @property
    def timeLabel(self):
        return f'Time t / {self.timeUnits}'

    def _parseFile(self, file: str) -> None:
        try:
            ws = load_workbook(str(file)).active
        except:
            raise ValueError

        self.metaData = self._parseMetaData(ws)
        valueUnits = self._parseValueUnits(ws)
        self.time = self._parseTime(ws)
        self._parseReactions(ws, valueUnits)

    def _parseMetaData(self, ws) -> None:
        metaData = {}
        for md, info in Plate._md.items():
            raw = ws[info['loc']].value
            groups = search(info['reg'], raw).groups()

            if md == 'Time':
                hours = int(groups[0]) + 12*int(groups[3] == 'PM')
                minutes = int(groups[1])
                seconds = int(groups[2])
                value = time(hours, minutes, seconds)
            elif md == 'Date':
                day = int(groups[1])
                month = int(groups[0])
                year = int(groups[2])
                value = date(year, month, day)
            else:
                value = groups[0]

            metaData.update({md: value})

        return metaData

    def _parseValueUnits(self, ws) -> str:
        return search(r'as (.*)$', ws['D12'].value).groups()[0]

    def _parseTime(self, ws):
        reg = r'Cycle \d* \((.* h)? ?(.* min)? ?(.* s)?\)'
        i = 16
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

    def _parseReactions(self, ws, units: str) -> None:
        start_row = 19
        start_col = 2
        delta = 4 + self.dimensions[0]
        self.reactions = []

        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                cycle = 0
                values = []
                while True:
                    value = ws.cell(start_row+row+cycle, start_col+col).value
                    if value:
                        values.append(value)
                        cycle += delta
                    else:
                        break
                index = row * self.dimensions[1] + col
                self.reactions.append(Reaction(self, values, index, units))
    