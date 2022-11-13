def str_to_bool(string: str):
    return str(string).lower() in ['@bool(true)', 'true', '1']
