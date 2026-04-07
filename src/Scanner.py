

class Scanner:

    def scan(self, codigo):
        tamanho_codigo = len(codigo)

        tokens = []

        count = 0

        token = ""

        symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "&", "|", "<", ">", "=", "~"]

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

            # Trata comentarios ANTES do restante
            if codigo[i] == '/' and i + 1 < tamanho_codigo:
                if codigo[i+1] == '/':
                    # Comentario de linha - ignora ate o fim da linha
                    if token != "":
                        tokens.append(token)
                        token = ""
                    i += 2
                    while i < tamanho_codigo and codigo[i] != '\n':
                        i += 1
                    continue
                elif codigo[i+1] == '*':
                    # Comentario de bloco - ignora ate */
                    if token != "":
                        tokens.append(token)
                        token = ""
                    i += 2
                    while i < tamanho_codigo - 1:
                        if codigo[i] == '*' and codigo[i+1] == '/':
                            i += 2
                            break
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

            # Trata simbolos (/ foi removido da lista)
            elif codigo[i] in symbols:
                if token != "":
                    tokens.append(token)
                    token = ""

                # Mantem simbolos como estao, sem conversao para XML
                tokens.append(codigo[i])
                
            # / sozinho (nao e comentario)
            elif codigo[i] == '/':
                if token != "":
                    tokens.append(token)
                    token = ""
                tokens.append('/')

            else:
                token = token + codigo[i]
            
            count += 1
            i += 1

        if token != "":
            tokens.append(token)

        return tokens