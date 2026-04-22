from src.scanner.Scanner import Scanner

entrada = r"tests\inputs\Main.jack"

scanner = Scanner(entrada)

xml_output = scanner.tokenizar()


print(xml_output)