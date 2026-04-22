from src.scanner.Scanner import Scanner
from src.parser.Parser import Parser

entrada = "input/Main.jack"

scanner = Scanner(entrada)

scanner.tokenizar()

tokens = scanner.get_tokens()

parser = Parser(tokens)
xml_output = parser.parse()

print(xml_output)

with open("output.xml", "w", encoding="utf-8") as f:
    f.write(xml_output)