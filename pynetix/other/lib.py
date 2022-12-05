def QBoolToBool(string: str):
    return str(string).lower() in ['@bool(true)', 'true', '1']