from src.parser.Grammar import Grammar


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.output = []
        self.indent_level = 0
        self.grammar = Grammar(self)

        self.classes = set()
        for token in self.tokens:
            if token.type == "identifier":
                self.classes.add(token.value)

    def get_class_names(self):
        return list(self.classes)

    def parse(self):
        self.grammar.parse_class()
        return "\n".join(self.output)

    def __getattr__(self, name):
        if name.startswith("parse_") and hasattr(self.grammar, name):
            return getattr(self.grammar, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # =========================
    # XML helpers
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
    # Token helpers
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
