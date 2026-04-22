

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
                self.parse_let()
            if self.match("keyword", "if"):
                # implementar parse_if()
                # self.parse_if()
                raise NotImplementedError("parse_if ainda nao implementado")
            if self.match("keyword", "while"):
                # implementar parse_while()
                # self.parse_while()
                raise NotImplementedError("parse_while ainda nao implementado")
            if self.match("keyword", "do"):
                self.parse_do()
            if self.match("keyword", "return"):
                self.parse_return()

    
    def parse_var_decl(self):
        self.consume("keyword", "var")
        self.consume("keyword", ["int", "char", "boolean"] + list(self.classes))
        self.consume("identifier")
        while self.match("symbol", ","):
            self.consume("symbol", ",")
            self.consume("identifier")
        self.consume("symbol", ";")
        
    def parse_let(self):
        self.consume("keyword", "let")
        self.consume("identifier")
        if self.match("symbol", "["):
            self.consume("symbol", "[")
            self.parse_expression()
            self.consume("symbol", "]")
        self.consume("symbol", "=")
        self.parse_expression()
        self.consume("symbol", ";")

    def parse_return(self):
        self.consume("keyword", "return")
        if not self.match("symbol", ";"):
            self.parse_expression()
        self.consume("symbol", ";")

    def parse_do(self):
        self.consume("keyword", "do")
        self.parse_subroutine_call()
        self.consume("symbol", ";")

    def parse_expression(self):
        self.parse_term()
        while self.match("symbol", ["+", "-", "*", "/", "&", "|", "<", ">", "="]):
            self.consume("symbol")
            self.parse_term()

    def parse_term(self):
        if self.match("integerConstant"):
            self.consume("integerConstant")
            return
        if self.match("stringConstant"):
            self.consume("stringConstant")
            return
        if self.match("keyword", ["true", "false", "null", "this"]):
            self.consume("keyword", ["true", "false", "null", "this"])
            return
        if self.match("symbol", "("):
            self.consume("symbol", "(")
            self.parse_expression()
            self.consume("symbol", ")")
            return
        if self.match("symbol", ["-", "~"]):
            self.consume("symbol", ["-", "~"])
            self.parse_term()
            return
        if self.match("identifier"):
            next_token = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
            if next_token and next_token.type == "symbol" and next_token.value == "[":
                self.consume("identifier")
                self.consume("symbol", "[")
                self.parse_expression()
                self.consume("symbol", "]")
                return
            if next_token and next_token.type == "symbol" and next_token.value in ("(", "."):
                self.parse_subroutine_call()
                return
            self.consume("identifier")
            return
        token_atual = self.peek()
        linha = token_atual.line if token_atual else "EOF"
        raise ValueError(f"Termo inesperado na linha {linha}")

    def parse_subroutine_call(self):
        self.consume("identifier")
        if self.match("symbol", "."):
            self.consume("symbol", ".")
            self.consume("identifier")
        self.consume("symbol", "(")
        self.parse_expression_list()
        self.consume("symbol", ")")

    def parse_expression_list(self):
        if not self.match("symbol", ")"):
            self.parse_expression()
            while self.match("symbol", ","):
                self.consume("symbol", ",")
                self.parse_expression()

    def parse_while(self):
        self.consume("keyword", "while")
        self.consume("symbol", "(")
        self.parse_expression()
        self.consume("symbol", ")")
        self.consume("symbol", "{")
        self.parse_statements()
        self.consume("symbol", "}")