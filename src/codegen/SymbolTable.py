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

    def start_subroutine(self, subroutine_type='function'):
        self._sub_table = {}
        self._counts['arg'] = 1 if subroutine_type == 'method' else 0
        self._counts['local'] = 0

    def define(self, name, type_, kind):
        entry = {'type': type_, 'kind': kind, 'index': self._counts[kind]}
        self._counts[kind] += 1
        if kind in ('static', 'field'):
            self._class_table[name] = entry
        else:
            self._sub_table[name] = entry

    def var_count(self, kind):
        return self._counts[kind]

    def _lookup(self, name):
        return self._sub_table.get(name) or self._class_table.get(name)

    def kind_of(self, name):
        entry = self._lookup(name)
        return entry['kind'] if entry else 'NONE'

    def type_of(self, name):
        entry = self._lookup(name)
        return entry['type'] if entry else None

    def index_of(self, name):
        entry = self._lookup(name)
        return entry['index'] if entry else None