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