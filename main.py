from src.utils import read_file
from src.Scanner import Scanner

codigo = read_file(r"tests\inputs\Main.jack")

scanner = Scanner()
tokens = scanner.extrair_tokens_brutos(codigo)
tokens_sem_comentarios = scanner.remover_comentarios(tokens)

scanner.validar_blocos(tokens_sem_comentarios)

tokens_classificados = scanner.classificar_tokens(tokens_sem_comentarios)

for token in tokens_classificados:
    print(token.type, token.value)

