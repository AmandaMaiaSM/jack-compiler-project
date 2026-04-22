

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

        self.classes = set()
        for token in self.tokens:
            if token.type == "identifier":
                self.classes.add(token.value)

    def get_class_names(self):
        return list(self.classes)

    def parse(self):
        pass

    # Métodos de Manipulação de Tokens

    def peek(self):
        if self.position < len(self.tokens):
            token_atual = self.tokens[self.position]
            return token_atual
        return None
    
    def consume(self, token_type=None, token_value=None):
        if not self.match(token_type, token_value):
            token_atual = self.peek()
            linha = token_atual.line if token_atual else "EOF"
            raise ValueError(f"Token inesperado na linha {linha}")
        return self.advance()
    
    def advance(self):
        token_atual = self.peek()
        if token_atual is not None:
            self.position += 1
        return token_atual

    def match(self, token_type=None, token_value=None):
        token_atual = self.peek()
        if token_atual is None:
            return False
        if token_type and token_atual.type != token_type:
            return False
        if token_value and token_atual.value != token_value:
            return False
        return True
