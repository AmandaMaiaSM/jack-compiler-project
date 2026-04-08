import sys
from src.JackTokenizer import JackTokenizer


entrada = r"tests\inputs\Main.jack"

compiler = JackTokenizer(entrada)
xml_output = compiler.tokenizar()

print(xml_output)