from src.scanner.Scanner import Scanner
from src.parser.Parser import Parser
from src.utils.WriterXML import WriterXML

entrada = "input/Main.jack"

scanner = Scanner(entrada)
scanner.tokenizar()
tokens = scanner.get_tokens()
tokens_xml = WriterXML().tokens_para_xml(tokens)

parser = Parser(tokens)

xml_output = parser.parse()

print(xml_output)

WriterXML().escrever_tokens(tokens, f"output/{entrada.split('/')[-1].replace('.jack', 'T.xml')}")
WriterXML().escrever_parser(xml_output, f"output/{entrada.split('/')[-1].replace('.jack', 'P.xml')}")
