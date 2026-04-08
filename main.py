import os
import sys

from src.utils import read_file
from src.Scanner import Scanner
from src.WriterXML import WriterXML

entrada = sys.argv[1] if len(sys.argv) > 1 else r"tests\inputs\Main.jack"
codigo = read_file(entrada)

scanner = Scanner()
tokens = scanner.extrair_tokens_brutos(codigo)
tokens_sem_comentarios = scanner.remover_comentarios(tokens)

scanner.validar_blocos(tokens_sem_comentarios)

tokens_classificados = scanner.classificar_tokens(tokens_sem_comentarios)

nome_base = os.path.splitext(os.path.basename(entrada))[0]
saida = os.path.join("output", f"{nome_base}T.xml")

writer_xml = WriterXML()
xml_texto = writer_xml.escrever_tokens(tokens_classificados, saida)
print(xml_texto)
print(f"XML salvo em: {saida}")