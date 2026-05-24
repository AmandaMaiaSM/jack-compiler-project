

class SymbolTable:
    # Mapeia a categoria da variável para o segmento de memória correspondente na VM
    KIND_TO_SEGMENT = {
        'field': 'this',
        'static': 'static',
        'arg': 'argument',
        'local': 'local',
    }

    # Inicializa as tabelas de escopo de classe e subrotina, e os contadores de índice
    def __init__(self):
        self._class_table = {}
        self._sub_table = {}
        self._counts = {'static': 0, 'field': 0, 'arg': 0, 'local': 0}

    # Inicia uma nova subrotina: zera o escopo local e ajusta o contador de arg (métodos reservam arg 0 para 'this')
    def start_subroutine(self, subroutine_type='function'):
        self._sub_table = {}
        self._counts['arg'] = 1 if subroutine_type == 'method' else 0
        self._counts['local'] = 0

    # Registra uma nova variável com tipo, categoria e índice; incrementa o contador da categoria
    def define(self, name, type_, kind):
        entry = {'type': type_, 'kind': kind, 'index': self._counts[kind]}
        self._counts[kind] += 1
        if kind in ('static', 'field'):
            self._class_table[name] = entry
        else:
            self._sub_table[name] = entry

    # Retorna quantas variáveis de uma dada categoria foram definidas até agora
    def var_count(self, kind):
        return self._counts[kind]

    # Busca a variável primeiro no escopo local e depois no escopo de classe (local tem prioridade)
    def _lookup(self, name):
        return self._sub_table.get(name) or self._class_table.get(name)

    # Retorna a categoria da variável (static, field, arg, local) ou 'NONE' se não declarada
    def kind_of(self, name):
        entry = self._lookup(name)
        return entry['kind'] if entry else 'NONE'

    # Retorna o tipo da variável (int, boolean, char ou nome de classe)
    def type_of(self, name):
        entry = self._lookup(name)
        return entry['type'] if entry else None

    # Retorna o índice da variável dentro do seu segmento de memória
    def index_of(self, name):
        entry = self._lookup(name)
        return entry['index'] if entry else None

    # Retorna o segmento VM correspondente à categoria da variável
    def segment_of(self, name):
        kind = self.kind_of(name)
        return self.KIND_TO_SEGMENT.get(kind)



