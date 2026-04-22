
class Token:
    def __init__(self, type, value, line=None):
        self.type = type
        self.value = value
        self.line = line

    def __str__(self):
        if self.line is None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type}, {self.value}, line={self.line})"