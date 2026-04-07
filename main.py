from src.utils import read_file
from src.Scanner import Scanner

codigo = read_file(r"tests\inputs\Main.jack")

scanner = Scanner()
tokens = scanner.extrair_tokens_brutos(codigo)
tokens_sem_comentarios = scanner.remover_comentarios(tokens)


# print("Tokens sem comentarios:")
# print(tokens_sem_comentarios)

scanner.classificar_tokens(tokens_sem_comentarios)

