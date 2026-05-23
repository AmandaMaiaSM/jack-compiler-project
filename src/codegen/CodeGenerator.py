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

    # ------------------------------------------------------------------ public

    def compile(self):
        self._compile_class()
        self._vm.close()

    # ----------------------------------------------------------------- helpers

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

    # --------------------------------------------------------------- class level

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

    # --------------------------------------------------------------- subroutine

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

    # --------------------------------------------------------------- statements

    def _compile_statements(self):
        dispatch = {
            'let': self._compile_let,
            'if': self._compile_if,
            'while': self._compile_while,
            'do': self._compile_do,
            'return': self._compile_return,
        }
        while self._match('keyword', tuple(dispatch)):
            kw = self._peek().value
            dispatch[kw]()

    def _compile_let(self):
        self._consume('keyword', 'let')
        var_name = self._consume('identifier').value
        is_array = self._match('symbol', '[')
        if is_array:
            self._consume('symbol', '[')
            self._push_var(var_name)        # push array base
            self._compile_expression()
            self._vm.write_arithmetic('add')  # base + index
            self._consume('symbol', ']')
        self._consume('symbol', '=')
        self._compile_expression()
        self._consume('symbol', ';')
        if is_array:
            self._vm.write_pop('temp', 0)     # save RHS value
            self._vm.write_pop('pointer', 1)  # set THAT to target address
            self._vm.write_push('temp', 0)    # restore value
            self._vm.write_pop('that', 0)     # store at arr[i]
        else:
            self._pop_var(var_name)

    def _compile_if(self):
        n = self._if_counter
        self._if_counter += 1
        self._consume('keyword', 'if')
        self._consume('symbol', '(')
        self._compile_expression()
        self._consume('symbol', ')')
        self._vm.write_arithmetic('not')
        self._vm.write_if_goto(f'IF_FALSE_{n}')
        self._consume('symbol', '{')
        self._compile_statements()
        self._consume('symbol', '}')
        self._vm.write_goto(f'IF_END_{n}')
        self._vm.write_label(f'IF_FALSE_{n}')
        if self._match('keyword', 'else'):
            self._consume('keyword', 'else')
            self._consume('symbol', '{')
            self._compile_statements()
            self._consume('symbol', '}')
        self._vm.write_label(f'IF_END_{n}')

    def _compile_while(self):
        n = self._while_counter
        self._while_counter += 1
        self._vm.write_label(f'WHILE_START_{n}')
        self._consume('keyword', 'while')
        self._consume('symbol', '(')
        self._compile_expression()
        self._consume('symbol', ')')
        self._vm.write_arithmetic('not')
        self._vm.write_if_goto(f'WHILE_END_{n}')
        self._consume('symbol', '{')
        self._compile_statements()
        self._consume('symbol', '}')
        self._vm.write_goto(f'WHILE_START_{n}')
        self._vm.write_label(f'WHILE_END_{n}')

    def _compile_do(self):
        self._consume('keyword', 'do')
        name = self._consume('identifier').value
        self._compile_subroutine_call(name)
        self._consume('symbol', ';')
        self._vm.write_pop('temp', 0)   # discard void return value

    def _compile_return(self):
        self._consume('keyword', 'return')
        if self._match('symbol', ';'):
            self._vm.write_push('constant', 0)   # void function returns 0
        else:
            self._compile_expression()
        self._consume('symbol', ';')
        self._vm.write_return()

    # --------------------------------------------------------------- expressions

    def _compile_expression(self):
        self._compile_term()
        while self._match('symbol', tuple(OP_MAP) + ('*', '/')):
            op = self._consume('symbol').value
            self._compile_term()
            if op == '*':
                self._vm.write_call('Math.multiply', 2)
            elif op == '/':
                self._vm.write_call('Math.divide', 2)
            else:
                self._vm.write_arithmetic(OP_MAP[op])

    def _compile_term(self):
        tok = self._peek()

        if tok.type == 'integerConstant':
            self._consume()
            self._vm.write_push('constant', int(tok.value))

        elif tok.type == 'stringConstant':
            self._consume()
            s = tok.value
            self._vm.write_push('constant', len(s))
            self._vm.write_call('String.new', 1)
            for ch in s:
                self._vm.write_push('constant', ord(ch))
                self._vm.write_call('String.appendChar', 2)

        elif tok.type == 'keyword' and tok.value in ('true', 'false', 'null', 'this'):
            self._consume()
            if tok.value == 'true':
                self._vm.write_push('constant', 0)
                self._vm.write_arithmetic('not')
            elif tok.value in ('false', 'null'):
                self._vm.write_push('constant', 0)
            else:  # this
                self._vm.write_push('pointer', 0)

        elif tok.type == 'symbol' and tok.value == '(':
            self._consume('symbol', '(')
            self._compile_expression()
            self._consume('symbol', ')')

        elif tok.type == 'symbol' and tok.value in ('-', '~'):
            op = self._consume('symbol').value
            self._compile_term()
            self._vm.write_arithmetic('neg' if op == '-' else 'not')

        elif tok.type == 'identifier':
            name = self._consume('identifier').value
            next_tok = self._peek()

            if next_tok and next_tok.value == '[':       # array access
                self._consume('symbol', '[')
                self._push_var(name)
                self._compile_expression()
                self._vm.write_arithmetic('add')
                self._consume('symbol', ']')
                self._vm.write_pop('pointer', 1)
                self._vm.write_push('that', 0)

            elif next_tok and next_tok.value in ('(', '.'):  # subroutine call
                self._compile_subroutine_call(name)

            else:                                         # simple variable
                self._push_var(name)

    def _compile_subroutine_call(self, name):
        next_tok = self._peek()

        if next_tok and next_tok.value == '.':
            self._consume('symbol', '.')
            method_name = self._consume('identifier').value
            if self._sym.kind_of(name) != 'NONE':
                # name is an object variable
                self._push_var(name)
                class_name = self._sym.type_of(name)
                self._consume('symbol', '(')
                n_args = self._compile_expression_list()
                self._consume('symbol', ')')
                self._vm.write_call(f'{class_name}.{method_name}', n_args + 1)
            else:
                # name is a class name — static function call
                self._consume('symbol', '(')
                n_args = self._compile_expression_list()
                self._consume('symbol', ')')
                self._vm.write_call(f'{name}.{method_name}', n_args)

        else:
            # Unqualified call — implicit this (method on current class)
            self._consume('symbol', '(')
            self._vm.write_push('pointer', 0)
            n_args = self._compile_expression_list()
            self._consume('symbol', ')')
            self._vm.write_call(f'{self._class_name}.{name}', n_args + 1)

    def _compile_expression_list(self):
        n = 0
        if not self._match('symbol', ')'):
            self._compile_expression()
            n += 1
            while self._match('symbol', ','):
                self._consume('symbol', ',')
                self._compile_expression()
                n += 1
        return n

    # --------------------------------------------------------------- utilities

    def _consume_type(self):
        tok = self._peek()
        if tok.type == 'keyword' and tok.value in ('int', 'char', 'boolean'):
            return self._consume('keyword').value
        return self._consume('identifier').value   # class name
