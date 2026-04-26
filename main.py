import os

from src.parser.Parser import Parser
from src.scanner.Scanner import Scanner
from src.utils.WriterXML import WriterXML

# Configuração de entrada e saída
entrada = "input/Main.jack"

# Etapa de análise léxica: tokenização
scanner = Scanner(entrada)
scanner.tokenizar()
tokens = scanner.get_tokens()

nome_base = os.path.splitext(os.path.basename(entrada))[0]

WriterXML().escrever_tokens(tokens, os.path.join("output", f"{nome_base}T.xml"))

# Etapa de análise sintática: parsing
parser = Parser(tokens)
xml_output = parser.parse()

arquivo_saida = os.path.join("output", f"{nome_base}P.xml")
WriterXML().escrever_parser(xml_output, arquivo_saida)

# Comparação com arquivo esperado
arquivo_esperado = os.path.join("expected", f"{nome_base}.xml")
resultado = WriterXML.comparar_arquivos(arquivo_saida, arquivo_esperado)

print(
	f"Comparação com arquivo esperado: "
	f"{'Sucesso, arquivos iguais' if resultado else 'Falha, arquivos diferentes'}"
)
