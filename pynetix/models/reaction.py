from numpy import array, stack


class Reaction:
    def __init__(self, plate, values, row: int, col: int, units='OD') -> None:
        self.plate = plate
        self.row = row
        self.col = col
        self.values = array(values)
        self.valueUnits = units

    @property
    def position(self):
        row = chr(self.row + 65)
        col = self.col % self.plate.dimensions[1]+1

        return f'{row}{col:d}'

    @property
    def data(self):
        return stack((self.time, self.values))

    @property
    def valueLabel(self):
        return f'Absorbance / {self.valueUnits}'

    @property
    def times(self):
        return self.plate.times

    @property
    def timeUnits(self):
        return self.plate.timeUnits

    @property
    def timeLabel(self):
        return self.plate.timeLabel

    def fit(self):
        pass
