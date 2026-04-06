
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.line = int

    def __str__(self):
        return f"Token({self.type}, {self.value})"