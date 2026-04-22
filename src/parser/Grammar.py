class Grammar:
    def __init__(self, parser):
        self.parser = parser

    # =========================
    # Grammar helpers
    # =========================

    def parse_type(self):
        if self.parser.match("keyword", ["int", "char", "boolean"]):
            self.parser.eat("keyword", ["int", "char", "boolean"])
        elif self.parser.match("identifier"):
            self.parser.eat("identifier")
        else:
            token_atual = self.parser.peek()
            linha = token_atual.line if token_atual else "EOF"
            valor = token_atual.value if token_atual else "EOF"
            raise ValueError(f"Tipo invalido na linha {linha}: {valor}")

    def parse_return_type(self):
        if self.parser.match("keyword", "void"):
            self.parser.eat("keyword", "void")
        else:
            self.parse_type()

    # =========================
    # Grammar rules
    # =========================

    def parse_class(self):
        self.parser.open_tag("class")

        self.parser.eat("keyword", "class")
        self.parser.eat("identifier")
        self.parser.eat("symbol", "{")

        while self.parser.match("keyword", ["static", "field"]):
            self.parse_class_var_decl()

        while self.parser.match("keyword", ["constructor", "function", "method"]):
            self.parse_subroutine_decl()

        self.parser.eat("symbol", "}")

        self.parser.close_tag("class")

    def parse_class_var_decl(self):
        self.parser.open_tag("classVarDec")

        self.parser.eat("keyword", ["static", "field"])
        self.parse_type()
        self.parser.eat("identifier")

        while self.parser.match("symbol", ","):
            self.parser.eat("symbol", ",")
            self.parser.eat("identifier")

        self.parser.eat("symbol", ";")

        self.parser.close_tag("classVarDec")

    def parse_subroutine_decl(self):
        self.parser.open_tag("subroutineDec")

        self.parser.eat("keyword", ["constructor", "function", "method"])
        self.parse_return_type()
        self.parser.eat("identifier")
        self.parser.eat("symbol", "(")
        self.parse_parameter_list()
        self.parser.eat("symbol", ")")
        self.parse_subroutine_body()

        self.parser.close_tag("subroutineDec")

    def parse_parameter_list(self):
        self.parser.open_tag("parameterList")

        if self.parser.match("keyword", ["int", "char", "boolean"]) or self.parser.match(
            "identifier"
        ):
            self.parse_type()
            self.parser.eat("identifier")

            while self.parser.match("symbol", ","):
                self.parser.eat("symbol", ",")
                self.parse_type()
                self.parser.eat("identifier")

        self.parser.close_tag("parameterList")

    def parse_subroutine_body(self):
        self.parser.open_tag("subroutineBody")

        self.parser.eat("symbol", "{")

        while self.parser.match("keyword", "var"):
            self.parse_var_decl()

        self.parse_statements()
        self.parser.eat("symbol", "}")

        self.parser.close_tag("subroutineBody")

    def parse_var_decl(self):
        self.parser.open_tag("varDec")

        self.parser.eat("keyword", "var")
        self.parse_type()
        self.parser.eat("identifier")

        while self.parser.match("symbol", ","):
            self.parser.eat("symbol", ",")
            self.parser.eat("identifier")

        self.parser.eat("symbol", ";")

        self.parser.close_tag("varDec")

    def parse_statements(self):
        self.parser.open_tag("statements")

        while self.parser.match("keyword", ["let", "if", "while", "do", "return"]):
            if self.parser.match("keyword", "let"):
                self.parse_let()
            elif self.parser.match("keyword", "if"):
                self.parse_if()
            elif self.parser.match("keyword", "while"):
                self.parse_while()
            elif self.parser.match("keyword", "do"):
                self.parse_do()
            elif self.parser.match("keyword", "return"):
                self.parse_return()

        self.parser.close_tag("statements")

    def parse_let(self):
        self.parser.open_tag("letStatement")

        self.parser.eat("keyword", "let")
        self.parser.eat("identifier")

        if self.parser.match("symbol", "["):
            self.parser.eat("symbol", "[")
            self.parse_expression()
            self.parser.eat("symbol", "]")

        self.parser.eat("symbol", "=")
        self.parse_expression()
        self.parser.eat("symbol", ";")

        self.parser.close_tag("letStatement")

    def parse_if(self):
        self.parser.open_tag("ifStatement")

        self.parser.eat("keyword", "if")
        self.parser.eat("symbol", "(")
        self.parse_expression()
        self.parser.eat("symbol", ")")
        self.parser.eat("symbol", "{")
        self.parse_statements()
        self.parser.eat("symbol", "}")

        if self.parser.match("keyword", "else"):
            self.parser.eat("keyword", "else")
            self.parser.eat("symbol", "{")
            self.parse_statements()
            self.parser.eat("symbol", "}")

        self.parser.close_tag("ifStatement")

    def parse_while(self):
        self.parser.open_tag("whileStatement")

        self.parser.eat("keyword", "while")
        self.parser.eat("symbol", "(")
        self.parse_expression()
        self.parser.eat("symbol", ")")
        self.parser.eat("symbol", "{")
        self.parse_statements()
        self.parser.eat("symbol", "}")

        self.parser.close_tag("whileStatement")

    def parse_do(self):
        self.parser.open_tag("doStatement")

        self.parser.eat("keyword", "do")
        self.parse_subroutine_call()
        self.parser.eat("symbol", ";")

        self.parser.close_tag("doStatement")

    def parse_return(self):
        self.parser.open_tag("returnStatement")

        self.parser.eat("keyword", "return")

        if not self.parser.match("symbol", ";"):
            self.parse_expression()

        self.parser.eat("symbol", ";")

        self.parser.close_tag("returnStatement")

    def parse_expression(self):
        self.parser.open_tag("expression")

        self.parse_term()

        while self.parser.match("symbol", ["+", "-", "*", "/", "&", "|", "<", ">", "="]):
            self.parser.eat("symbol")
            self.parse_term()

        self.parser.close_tag("expression")

    def parse_term(self):
        self.parser.open_tag("term")

        if self.parser.match("integerConstant"):
            self.parser.eat("integerConstant")
            self.parser.close_tag("term")
            return

        if self.parser.match("stringConstant"):
            self.parser.eat("stringConstant")
            self.parser.close_tag("term")
            return

        if self.parser.match("keyword", ["true", "false", "null", "this"]):
            self.parser.eat("keyword", ["true", "false", "null", "this"])
            self.parser.close_tag("term")
            return

        if self.parser.match("symbol", "("):
            self.parser.eat("symbol", "(")
            self.parse_expression()
            self.parser.eat("symbol", ")")
            self.parser.close_tag("term")
            return

        if self.parser.match("symbol", ["-", "~"]):
            self.parser.eat("symbol", ["-", "~"])
            self.parse_term()
            self.parser.close_tag("term")
            return

        if self.parser.match("identifier"):
            next_token = (
                self.parser.tokens[self.parser.position + 1]
                if self.parser.position + 1 < len(self.parser.tokens)
                else None
            )

            if next_token and next_token.type == "symbol" and next_token.value == "[":
                self.parser.eat("identifier")
                self.parser.eat("symbol", "[")
                self.parse_expression()
                self.parser.eat("symbol", "]")
                self.parser.close_tag("term")
                return

            if next_token and next_token.type == "symbol" and next_token.value in ("(", "."):
                self.parse_subroutine_call()
                self.parser.close_tag("term")
                return

            self.parser.eat("identifier")
            self.parser.close_tag("term")
            return

        token_atual = self.parser.peek()
        linha = token_atual.line if token_atual else "EOF"
        valor = token_atual.value if token_atual else "EOF"
        raise ValueError(f"Termo inesperado na linha {linha}: {valor}")

    def parse_subroutine_call(self):
        self.parser.eat("identifier")

        if self.parser.match("symbol", "."):
            self.parser.eat("symbol", ".")
            self.parser.eat("identifier")

        self.parser.eat("symbol", "(")
        self.parse_expression_list()
        self.parser.eat("symbol", ")")

    def parse_expression_list(self):
        self.parser.open_tag("expressionList")

        if not self.parser.match("symbol", ")"):
            self.parse_expression()

            while self.parser.match("symbol", ","):
                self.parser.eat("symbol", ",")
                self.parse_expression()

        self.parser.close_tag("expressionList")
