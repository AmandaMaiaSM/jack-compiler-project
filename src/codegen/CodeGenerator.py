from src.parser.Parser import Parser
from src.codegen.SymbolTable import SymbolTable
from src.codegen.VMWriter import VMWriter

OP_MAP = {
    '+': 'add', '-': 'sub', '&': 'and', '|': 'or',
    '<': 'lt', '>': 'gt', '=': 'eq',
}

class CodeGenerator:
    def __init__(self, tokens, output_path):
        self._parser = Parser(tokens)
        self._sym = SymbolTable()
        self._vm = VMWriter(output_path)
        self._class_name = ''
        self._sub_type = ''
        self._if_counter = 0
        self._while_counter = 0

    def compile(self):
        self._compile_class()
        self._vm.close()

    def _consume(self, token_type=None, token_value=None):
        return self._parser.consume(token_type, token_value)

    def _peek(self):
        return self._parser.peek()

    def _match(self, token_type=None, token_value=None):
        return self._parser.match(token_type, token_value)

    def _push_var(self, name):
        self._vm.write_push(self._sym.segment_of(name), self._sym.index_of(name))

    def _pop_var(self, name):
        self._vm.write_pop(self._sym.segment_of(name), self._sym.index_of(name))

    def _compile_class(self):
        self._consume('keyword', 'class')
        self._class_name = self._consume('identifier').value
        self._consume('symbol', '{')
        while self._match('keyword', ('static', 'field')):
            self._compile_class_var_decl()
        while self._match('keyword', ('constructor', 'function', 'method')):
            self._compile_subroutine()
        self._consume('symbol', '}')

    def _compile_class_var_decl(self):
        kind = self._consume('keyword').value          # static | field
        type_ = self._consume_type()
        name = self._consume('identifier').value
        self._sym.define(name, type_, kind)
        while self._match('symbol', ','):
            self._consume('symbol', ',')
            name = self._consume('identifier').value
            self._sym.define(name, type_, kind)
        self._consume('symbol', ';')