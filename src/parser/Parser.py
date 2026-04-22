

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
        return self.parse_class()

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
        if token_value is not None:
            if isinstance(token_value, (list, tuple, set)):
                if token_atual.value not in token_value:
                    return False
            else:
                if token_atual.value != token_value:
                    return False
        return True


    ## Métodos da Gramática

    def parse_class(self):
        self.consume("keyword", "class")
        self.consume("identifier")
        self.consume("symbol", "{")
        while self.match("keyword", ["static", "field"]):
            self.parse_class_var_decl()
        while self.match("keyword", ["constructor", "function", "method"]):
            self.parse_subroutine_decl()
        self.consume("symbol", "}")

    ### Regra de variável de classe

    def parse_class_var_decl(self):
        self.consume("keyword", ["static", "field"])
        self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
        self.consume("identifier")
        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")
        self.consume("symbol", ";")

    # Regra de declaração de metodos, funções e construtores

    def parse_subroutine_decl(self):
        self.consume("keyword", ["constructor", "function", "method"])
        self.consume("keyword", ["void", "int", "char", "boolean"] + list(self.classes))
        self.consume("identifier")
        self.consume("symbol", "(")
        self.parse_parameter_list()
        self.consume("symbol", ")")
        self.parse_subroutine_body()

    def parse_parameter_list(self):
        if self.match("keyword", ["int", "char", "boolean"] + list(self.classes)):
            self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
            self.consume("identifier")
            while self.match("symbol", ","):
                self.consume("symbol", ",")
                self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
                self.consume("identifier")

    def parse_subroutine_body(self):
        self.consume("symbol", "{")
        while self.match("keyword", "var"):
            self.parse_var_decl()
        self.parse_statements()
        self.consume("symbol", "}")

    def parse_statements(self):
        while self.match("keyword", ["let", "if", "while", "do", "return"]):
            if self.match("keyword", "let"):
                # implementar parse_let()
                # self.parse_let()
                raise NotImplementedError("parse_let ainda nao implementado")
            if self.match("keyword", "if"):
                # implementar parse_if()
                # self.parse_if()
                raise NotImplementedError("parse_if ainda nao implementado")
            if self.match("keyword", "while"):
                # implementar parse_while()
                # self.parse_while()
                raise NotImplementedError("parse_while ainda nao implementado")
            if self.match("keyword", "do"):
                # implementar parse_do()
                # self.parse_do()
                raise NotImplementedError("parse_do ainda nao implementado")
            if self.match("keyword", "return"):
                # implementar parse_return()
                # self.parse_return()
                raise NotImplementedError("parse_return ainda nao implementado")

    def parse_var_decl(self):
        self.consume("keyword", "var")
        self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
        self.consume("identifier")
        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")
        self.consume("symbol", ";")