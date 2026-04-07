from src.utils import read_file
from src.Scanner import Scanner

codigo = read_file(r"tests\inputs\Main.jack")

scanner = Scanner()
tokens = scanner.scan(codigo)

print(tokens)