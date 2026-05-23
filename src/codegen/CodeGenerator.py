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


    def _compile_subroutine(self):
        self._sub_type = self._consume('keyword').value   # constructor|function|method
        self._consume()                                    # return type
        sub_name = self._consume('identifier').value
        self._consume('symbol', '(')
        self._sym.start_subroutine(self._sub_type)
        self._compile_parameter_list()
        self._consume('symbol', ')')
        self._compile_subroutine_body(sub_name)

    def _compile_parameter_list(self):
        if self._match('symbol', ')'):
            return
        type_ = self._consume_type()
        name = self._consume('identifier').value
        self._sym.define(name, type_, 'arg')
        while self._match('symbol', ','):
            self._consume('symbol', ',')
            type_ = self._consume_type()
            name = self._consume('identifier').value
            self._sym.define(name, type_, 'arg')

    def _compile_subroutine_body(self, sub_name):
        self._consume('symbol', '{')
        # Collect var declarations BEFORE emitting function header (need nLocals)
        while self._match('keyword', 'var'):
            self._compile_var_decl()
        n_locals = self._sym.var_count('local')
        self._vm.write_function(f'{self._class_name}.{sub_name}', n_locals)
        self._emit_subroutine_prologue()
        self._compile_statements()
        self._consume('symbol', '}')

    def _emit_subroutine_prologue(self):
        if self._sub_type == 'constructor':
            n_fields = self._sym.var_count('field')
            self._vm.write_push('constant', n_fields)
            self._vm.write_call('Memory.alloc', 1)
            self._vm.write_pop('pointer', 0)
        elif self._sub_type == 'method':
            self._vm.write_push('argument', 0)
            self._vm.write_pop('pointer', 0)

    def _compile_var_decl(self):
        self._consume('keyword', 'var')
        type_ = self._consume_type()
        name = self._consume('identifier').value
        self._sym.define(name, type_, 'local')
        while self._match('symbol', ','):
            self._consume('symbol', ',')
            name = self._consume('identifier').value
            self._sym.define(name, type_, 'local')
        self._consume('symbol', ';')