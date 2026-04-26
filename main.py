from src.scanner.Scanner import Scanner
from src.parser.Parser import Parser
from src.utils.WriterXML import WriterXML

# Configuração de entrada e saída
entrada = "input/Main.jack"

# Etapa de Análise Léxica: Tokenização
scanner = Scanner(entrada)
scanner.tokenizar()
tokens = scanner.get_tokens()

WriterXML().escrever_tokens(
    tokens, 
    f"output/{entrada.split('/')[-1].replace('.jack', 'T.xml')}"
)

# Etapa de Análise Sintática: Parsing
parser = Parser(tokens)
xml_output = parser.parse()
arquivo_saida = f"output/{entrada.split('/')[-1].replace('.jack', 'P.xml')}"

WriterXML().escrever_parser(
    xml_output, 
    arquivo_saida
)

# Comparação com arquivo esperado
arquivo_esperado = f"expected/{entrada.split('/')[-1].replace('.jack', '.xml')}"

resultado = WriterXML.comparar_arquivos(
    arquivo_saida, 
    arquivo_esperado
) 

print(f"Comparação com arquivo esperado: {'Sucesso, arquivos iguais' if resultado else 'Falha, arquivos diferentes'}")