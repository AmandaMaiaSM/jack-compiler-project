class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.output = []
        self.indent_level = 0

        self.classes = set()
        for token in self.tokens:
            if token.type == "identifier":
                self.classes.add(token.value)

    def get_class_names(self):
        return list(self.classes)

    def parse(self):
        self.parse_class()
        return "\n".join(self.output)

    # =========================
    # Utilitários de XML
    # =========================

    def write_line(self, content):
        self.output.append("  " * self.indent_level + content)

    def open_tag(self, tag_name):
        self.write_line(f"<{tag_name}>")
        self.indent_level += 1

    def close_tag(self, tag_name):
        self.indent_level -= 1
        self.write_line(f"</{tag_name}>")

    def escape_xml(self, value):
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def write_token_xml(self, token):
        valor = self.escape_xml(token.value)
        self.write_line(f"<{token.type}> {valor} </{token.type}>")

    # =========================
    # Métodos de Manipulação de Tokens
    # =========================

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

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

    def consume(self, token_type=None, token_value=None):
        if not self.match(token_type, token_value):
            token_atual = self.peek()
            linha = token_atual.line if token_atual else "EOF"
            valor = token_atual.value if token_atual else "EOF"
            tipo = token_atual.type if token_atual else "EOF"
            raise ValueError(
                f"Token inesperado na linha {linha}: valor='{valor}', tipo='{tipo}'"
            )
        return self.advance()

    def eat(self, token_type=None, token_value=None):
        token = self.consume(token_type, token_value)
        self.write_token_xml(token)
        return token

    # =========================
    # Auxiliares da gramática
    # =========================

    def parse_type(self):
        if self.match("keyword", ["int", "char", "boolean"]):
            self.eat("keyword", ["int", "char", "boolean"])
        elif self.match("identifier"):
            self.eat("identifier")
        else:
            token_atual = self.peek()
            linha = token_atual.line if token_atual else "EOF"
            valor = token_atual.value if token_atual else "EOF"
            raise ValueError(f"Tipo inválido na linha {linha}: {valor}")

    def parse_return_type(self):
        if self.match("keyword", "void"):
            self.eat("keyword", "void")
        else:
            self.parse_type()

    # =========================
    # Métodos da Gramática
    # =========================

    def parse_class(self):
        self.open_tag("class")

        self.eat("keyword", "class")
        self.eat("identifier")
        self.eat("symbol", "{")

        while self.match("keyword", ["static", "field"]):
            self.parse_class_var_decl()

        while self.match("keyword", ["constructor", "function", "method"]):
            self.parse_subroutine_decl()

        self.eat("symbol", "}")

        self.close_tag("class")

    def parse_class_var_decl(self):
        self.open_tag("classVarDec")

        self.eat("keyword", ["static", "field"])
        self.parse_type()
        self.eat("identifier")

        while self.match("symbol", ","):
            self.eat("symbol", ",")
            self.eat("identifier")

        self.eat("symbol", ";")

        self.close_tag("classVarDec")

    def parse_subroutine_decl(self):
        self.open_tag("subroutineDec")

        self.eat("keyword", ["constructor", "function", "method"])
        self.parse_return_type()
        self.eat("identifier")
        self.eat("symbol", "(")
        self.parse_parameter_list()
        self.eat("symbol", ")")
        self.parse_subroutine_body()

        self.close_tag("subroutineDec")

    def parse_parameter_list(self):
        self.open_tag("parameterList")

        if self.match("keyword", ["int", "char", "boolean"]) or self.match("identifier"):
            self.parse_type()
            self.eat("identifier")

            while self.match("symbol", ","):
                self.eat("symbol", ",")
                self.parse_type()
                self.eat("identifier")

        self.close_tag("parameterList")

    def parse_subroutine_body(self):
        self.open_tag("subroutineBody")

        self.eat("symbol", "{")

        while self.match("keyword", "var"):
            self.parse_var_decl()

        self.parse_statements()
        self.eat("symbol", "}")

        self.close_tag("subroutineBody")

    def parse_var_decl(self):
        self.open_tag("varDec")

        self.eat("keyword", "var")
        self.parse_type()
        self.eat("identifier")

        while self.match("symbol", ","):
            self.eat("symbol", ",")
            self.eat("identifier")

        self.eat("symbol", ";")

        self.close_tag("varDec")

    def parse_statements(self):
        self.open_tag("statements")

        while self.match("keyword", ["let", "if", "while", "do", "return"]):
            if self.match("keyword", "let"):
                self.parse_let()
            elif self.match("keyword", "if"):
                self.parse_if()
            elif self.match("keyword", "while"):
                self.parse_while()
            elif self.match("keyword", "do"):
                self.parse_do()
            elif self.match("keyword", "return"):
                self.parse_return()

        self.close_tag("statements")

    def parse_let(self):
        self.open_tag("letStatement")

        self.eat("keyword", "let")
        self.eat("identifier")

        if self.match("symbol", "["):
            self.eat("symbol", "[")
            self.parse_expression()
            self.eat("symbol", "]")

        self.eat("symbol", "=")
        self.parse_expression()
        self.eat("symbol", ";")

        self.close_tag("letStatement")

    def parse_if(self):
        self.open_tag("ifStatement")

        self.eat("keyword", "if")
        self.eat("symbol", "(")
        self.parse_expression()
        self.eat("symbol", ")")
        self.eat("symbol", "{")
        self.parse_statements()
        self.eat("symbol", "}")

        if self.match("keyword", "else"):
            self.eat("keyword", "else")
            self.eat("symbol", "{")
            self.parse_statements()
            self.eat("symbol", "}")

        self.close_tag("ifStatement")

    def parse_while(self):
        self.open_tag("whileStatement")

        self.eat("keyword", "while")
        self.eat("symbol", "(")
        self.parse_expression()
        self.eat("symbol", ")")
        self.eat("symbol", "{")
        self.parse_statements()
        self.eat("symbol", "}")

        self.close_tag("whileStatement")

    def parse_do(self):
        self.open_tag("doStatement")

        self.eat("keyword", "do")
        self.parse_subroutine_call()
        self.eat("symbol", ";")

        self.close_tag("doStatement")

    def parse_return(self):
        self.open_tag("returnStatement")

        self.eat("keyword", "return")

        if not self.match("symbol", ";"):
            self.parse_expression()

        self.eat("symbol", ";")

        self.close_tag("returnStatement")

    def parse_expression(self):
        self.open_tag("expression")

        self.parse_term()

        while self.match("symbol", ["+", "-", "*", "/", "&", "|", "<", ">", "="]):
            self.eat("symbol")
            self.parse_term()

        self.close_tag("expression")

    def parse_term(self):
        self.open_tag("term")

        if self.match("integerConstant"):
            self.eat("integerConstant")
            self.close_tag("term")
            return

        if self.match("stringConstant"):
            self.eat("stringConstant")
            self.close_tag("term")
            return

        if self.match("keyword", ["true", "false", "null", "this"]):
            self.eat("keyword", ["true", "false", "null", "this"])
            self.close_tag("term")
            return

        if self.match("symbol", "("):
            self.eat("symbol", "(")
            self.parse_expression()
            self.eat("symbol", ")")
            self.close_tag("term")
            return

        if self.match("symbol", ["-", "~"]):
            self.eat("symbol", ["-", "~"])
            self.parse_term()
            self.close_tag("term")
            return

        if self.match("identifier"):
            next_token = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None

            if next_token and next_token.type == "symbol" and next_token.value == "[":
                self.eat("identifier")
                self.eat("symbol", "[")
                self.parse_expression()
                self.eat("symbol", "]")
                self.close_tag("term")
                return

            if next_token and next_token.type == "symbol" and next_token.value in ("(", "."):
                self.parse_subroutine_call()
                self.close_tag("term")
                return

            self.eat("identifier")
            self.close_tag("term")
            return

        token_atual = self.peek()
        linha = token_atual.line if token_atual else "EOF"
        valor = token_atual.value if token_atual else "EOF"
        raise ValueError(f"Termo inesperado na linha {linha}: {valor}")

    def parse_subroutine_call(self):
        self.eat("identifier")

        if self.match("symbol", "."):
            self.eat("symbol", ".")
            self.eat("identifier")

        self.eat("symbol", "(")
        self.parse_expression_list()
        self.eat("symbol", ")")

    def parse_expression_list(self):
        self.open_tag("expressionList")

        if not self.match("symbol", ")"):
            self.parse_expression()

            while self.match("symbol", ","):
                self.eat("symbol", ",")
                self.parse_expression()

        self.close_tag("expressionList")