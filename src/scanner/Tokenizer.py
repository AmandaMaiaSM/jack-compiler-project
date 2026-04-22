

from src.scanner.Token import Token


class Tokenizer:

    def __init__(self):
        self.symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
        self.keywords = ["CLASS", "CONSTRUCTOR", "FUNCTION", "METHOD", "FIELD", 
            "STATIC", "VAR", "INT", "CHAR", "BOOLEAN", "VOID", 
            "TRUE", "FALSE", "NULL", "THIS", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN"
            ]
        
    def scan(self, codigo):
        return self.extrair_tokens_brutos(codigo)

    def extrair_tokens_brutos(self, codigo):
        tamanho_codigo = len(codigo)

        tokens = []

        token = ""

        i = 0
        while i < tamanho_codigo:
            # Primeiro, trata strings
            if codigo[i] == '"':
                if token != "":
                    tokens.append(token)
                    token = ""

                i += 1
                string_val = ""
                while i < tamanho_codigo and codigo[i] != '"':
                    string_val += codigo[i]
                    i += 1

                tokens.append('"')
                tokens.append(string_val)
                if i < tamanho_codigo and codigo[i] == '"':
                    tokens.append('"')
                    i += 1
                continue

            # Trata espacos em branco
            if codigo[i] in {" ", "\n", "\t", "\r"}:
                token = token.strip()

                if token != "":
                    tokens.append(token)

                if codigo[i] == "\n":
                    tokens.append("\n")

                token = ""

            # Trata simbolos (incluindo /)
            elif codigo[i] in self.symbols:
                if token != "":
                    tokens.append(token)
                    token = ""

                # Mantem simbolos como estao, sem conversao para XML
                tokens.append(codigo[i])

            else:
                token = token + codigo[i]

            i += 1

        if token != "":
            tokens.append(token)

        return tokens

    def remover_comentarios(self, tokens):
        tokens_sem_comentarios = []
        i = 0
        em_comentario_bloco = False
        em_comentario_linha = False

        while i < len(tokens):
            token_atual = tokens[i]

            if em_comentario_bloco:
                if token_atual == '*' and i + 1 < len(tokens) and tokens[i + 1] == '/':
                    em_comentario_bloco = False
                    i += 2
                    continue
                if token_atual == "\n":
                    tokens_sem_comentarios.append(token_atual)
                i += 1
                continue

            if em_comentario_linha:
                if token_atual == "\n":
                    em_comentario_linha = False
                    tokens_sem_comentarios.append(token_atual)
                i += 1
                continue

            if token_atual == '/' and i + 1 < len(tokens):
                proximo = tokens[i + 1]
                if proximo == '/':
                    em_comentario_linha = True
                    i += 2
                    continue
                if proximo == '*':
                    em_comentario_bloco = True
                    i += 2
                    continue

            tokens_sem_comentarios.append(token_atual)
            i += 1

        return tokens_sem_comentarios
    
    def classificar_tokens(self, tokens=None):

        if tokens is None:
            tokens = []

        quantidade_tokens = len(tokens)
        tokens_classificados = []
        
        i = 0
        linha = 1
        while i < quantidade_tokens:
            if tokens[i] == "\n":
                linha += 1
                i += 1
                continue

            if tokens[i] == '"':
                if i + 1 < quantidade_tokens:
                    string_val = tokens[i + 1]
                    tokens_classificados.append(Token("stringConstant", string_val, linha))
                    i += 1
                if i + 1 < quantidade_tokens and tokens[i + 1] == '"':
                    i += 1
                i += 1
                continue
        
            if tokens[i].upper() in self.keywords:
                tokens_classificados.append(Token("keyword", tokens[i], linha))
            elif tokens[i].upper() in self.symbols:
                tokens_classificados.append(Token("symbol", tokens[i], linha))
            elif tokens[i].isdigit():
                tokens_classificados.append(Token("integerConstant", tokens[i], linha))
            else:
                tokens_classificados.append(Token("identifier", tokens[i], linha))

            i += 1

        return tokens_classificados


    def validar_blocos(self, tokens=None):

        if tokens is None:
            tokens = []

        abertura_para_fechamento = {
            "{": "}",
            "(": ")",
            "[": "]",
            '"': '"'
        }
        fechamentos = set(abertura_para_fechamento.values())
        pilha = []
        for token in tokens:
            if token == "\n":
                continue

            if token == '"':
                if pilha and pilha[-1] == '"':
                    pilha.pop()
                else:
                    pilha.append('"')
                continue

            if pilha and pilha[-1] == '"':
                continue

            if token in abertura_para_fechamento:
                pilha.append(token)
                continue

            if token in fechamentos:
                if not pilha:
                    raise ValueError(f"Erro: fechamento inesperado {token}")

                topo = pilha[-1]
                esperado = abertura_para_fechamento.get(topo)
                if token == esperado:
                    pilha.pop()
                else:
                    raise ValueError(f"Erro: esperado {esperado} mas encontrou {token}")

        if pilha:
            aberto = pilha[-1]
            esperado = abertura_para_fechamento.get(aberto)
            if aberto == '"':
                raise ValueError('Erro: string nao fechada com "')
            raise ValueError(f"Erro: bloco nao fechado, esperado {esperado}")
        
    
