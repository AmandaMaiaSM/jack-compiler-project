class SymbolTable:
    KIND_TO_SEGMENT = {
        'field': 'this',
        'static': 'static',
        'arg': 'argument',
        'local': 'local',
    }

    def __init__(self):
        self._class_table = {}
        self._sub_table = {}
        self._counts = {'static': 0, 'field': 0, 'arg': 0, 'local': 0}

