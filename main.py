from src.utils import read_file

texto = repr(read_file(r"tests\inputs\Main.jack"))
texto = texto[1:-1]
texto = texto.replace("\\n", "\n")

tamanho_texto = len(texto)

tokens = []

count = 0

token = ""

symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

i = 0
while i < tamanho_texto:
    if texto[i] == '"':
        if token != "":
            tokens.append(token)
            token = ""

        i += 1
        string_val = ""
        while i < tamanho_texto and texto[i] != '"':
            string_val += texto[i]
            i += 1

        tokens.append(string_val)
        i += 1
        continue

    if texto[i] in {" ", "\n", "\t", "\r"}:
    
        token = token.strip()

        if token != "":
            tokens.append(token)

        if texto[i] == "\n":
            tokens.append("\n")

        token = ""

    elif texto[i] in symbols:
        if token != "":
            tokens.append(token)
            token = ""

        if texto[i] == '"':
            tokens.append("&quot;")
        elif texto[i] == '>':
            tokens.append("&gt;") 
        elif texto[i] == '<':
            tokens.append("&lt;")
        elif texto[i] == '&':
            tokens.append('&amp;')
        elif texto[i] == '/':
            if i + 1 < tamanho_texto and texto[i+1] == '/':
                tokens.append('//')
                i += 2
                continue
            elif i + 1 < tamanho_texto and texto[i+1] == '*':
                tokens.append('/*')
                i += 2
                continue
            else:
                tokens.append('/')

        elif texto[i] == '*':
            if i + 1 < tamanho_texto and texto[i+1] == '/':
                tokens.append('*/')
                i += 2
                continue
            else:
                tokens.append('*')

        else:
            tokens.append(texto[i])
         
    else:
        token = token + texto[i]
    
    count += 1
    i += 1

if token != "":
    tokens.append(token)

tokens_sem_comentario = []
em_bloco = False
for tok in tokens:
    if tok == '/*':
        em_bloco = True
        continue
    if tok == '*/':
        em_bloco = False
        continue
    if not em_bloco:
        tokens_sem_comentario.append(tok)

linhas = []
linha_atual = []

for tok in tokens_sem_comentario:
    if tok == "\n":
        if linha_atual:
            linhas.append(linha_atual)
            linha_atual = []
    else:
        linha_atual.append(tok)

if linha_atual:
    linhas.append(linha_atual)

linhas_limpas = []
for linha in linhas:
    if linha[0] == '//':
        continue

    nova_linha = []
    for tok in linha:
        if tok == '//':
            break
        nova_linha.append(tok)

    if nova_linha:
        linhas_limpas.append(nova_linha)

for linha in linhas_limpas:
    print(linha)