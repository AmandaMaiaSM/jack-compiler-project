

class Scanner:

    def scan(self, codigo):
        return self.extrair_tokens_brutos(codigo)

    def extrair_tokens_brutos(self, codigo):
        tamanho_codigo = len(codigo)

        tokens = []

        token = ""

        symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

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

                tokens.append(string_val)
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
            elif codigo[i] in symbols:
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