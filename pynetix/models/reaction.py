from numpy import array, stack


class Reaction:
    def __init__(self, plate, values, index: int, units='OD') -> None:
        self.plate = plate
        self.index = index
        self.values = array(values)
        self.valueUnits = units

    @property
    def position(self):
        row = self.index // 12  # self.plate.dimensions[1]
        row = chr(row + 65)
        col = self.index % 12+1  # self.plate.dimensions[1]

        return f'{row}{col:d}'

    @property
    def data(self):
        return stack((self.time, self.values))

    @property
    def valueLabel(self):
        return f'Absorbance / {self.valueUnits}'

    @property
    def time(self):
        return self.plate.time

    @property
    def timeUnits(self):
        return self.plate.timeUnits

    @property
    def timeLabel(self):
        return self.plate.timeLabel

    def fit(self):
        pass
