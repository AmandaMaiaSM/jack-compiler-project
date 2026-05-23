from src.parser.Parser import Parser

OP_MAP = {
    '+': 'add', '-': 'sub', '&': 'and', '|': 'or',
    '<': 'lt', '>': 'gt', '=': 'eq',
}

class CodeGenerator:
    def __init__(self, parser: Parser):
        self.parser = parser