class Standard:
    metaData = {'User': {'loc': 'A3', 'name': 'User'},
          'Path': {'loc': 'A4', 'name': 'Path'},
          'Test ID': {'loc': 'A5', 'name': 'Test ID'},
          'Test Name': {'loc': 'A6', 'name': 'Test Name'},
          'Date': {'loc': 'A7', 'name': 'Date'},
          'Time': {'loc': 'A8', 'name': 'Time'},
          'ID1': {'loc': 'A9', 'name': 'ID1'},
          'ID2': {'loc': 'A10', 'name': 'ID2'},
          'ID3': {'loc': 'A11', 'name': 'ID3'}}
    valueUnits = 'D12'
    timeLoc = 16
    startRow = 19
    startCol = 2

class New(Standard):
    metaData = {'User': {'loc': 'A3', 'name': 'User'},
          'Path': {'loc': 'A4', 'name': 'Path'},
          'Test ID': {'loc': 'A5', 'name': 'Test ID'},
          'Test Name': {'loc': 'A6', 'name': 'Test Name'},
          'Date': {'loc': 'A7', 'name': 'Date'},
          'Time': {'loc': 'A8', 'name': 'Time'}}
    valueUnits = 'D9'
    startRow = 16
    timeLoc = 13