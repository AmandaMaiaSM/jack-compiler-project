from src.utils import read_file

texto = repr(read_file(r"tests\inputs\Main.jack"))
texto = texto[1:-1]
texto = texto.replace("\\n", "\n")

tokens = []

token = ""

for i in texto:
    if i == " " or i == "\n":
    
        token = token.strip()
        if token != "":
            tokens.append(token)

        if i == "\n":
            tokens.append("\n")

        token = ""
    else:
        token = token + i

    
print(tokens)