from re import search

from numpy import argmin, array


def QBoolToBool(value: str):
    if isinstance(value, str):
        return str(value).lower() in ['@bool(true)', 'true', '1']
    else:
        return value


def QListToList(value: str):
    if isinstance(value, str):
        return search(r'@List\((.*)\)$', value).groups()[0].split()
    else:
        return value


def ListToQList(values):
    out = '@List('
    for value in values:
        out += str(value) + ' '
    out = out[:-1] + ')'
    return out


def closestValue(target, list_):
    return argmin(abs(array(list_)-target))
