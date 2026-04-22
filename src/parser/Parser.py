

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
        if token_value is None:
            if isinstance(token_value, (list, tuple, set)):
                if token_atual.value not in token_value:
                    return False
                else: 
                    if token_atual.value != token_value:
                        return False
        return True


    ## Métodos da Gramática

    ### Regra de variável de classe

    def parse_class_var_decl(self):
        self.consume("keyword", ["static", "field"])
        self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
        self.consume("identifier")
        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")
        self.consume("symbol", ";")
