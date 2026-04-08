# jack-compiler-project
### Jack Compiler

## Descricao
Este projeto implementa um compilador para a linguagem Jack (Nand2Tetris), com foco inicial na etapa de analise lexica. O tokenizer le arquivos `.jack`, remove comentarios, valida delimitadores e gera tokens que podem ser exportados em XML.

## Integrantes
- Amanda Maia Soares Silva
- Marcos Antonio Branco Pereira Junior

## Linguagem utilizada
Python

## Etapas do projeto
1. Analisador Lexico (Tokenizer)
2. Analisador Sintatico (Parser)
3. Geracao de Codigo (VM)

## Como rodar
1. Escolha o arquivo de entrada em `main.py` (ex.: `tests\inputs\Main.jack`).
2. Execute:

```bash
python main.py
```

O XML de tokens e salvo em `output/` com o sufixo `T.xml`.

## Descricao dos arquivos
- `main.py`: ponto de entrada que executa o tokenizer e imprime o XML.
- `src/JackTokenizer.py`: orquestra leitura, tokenizacao, validacao e escrita do XML.
- `src/Scanner.py`: implementa a analise lexica (tokenizacao, remocao de comentarios e validacao de blocos).
- `src/Token.py`: classe `Token` para representar tipo, valor e linha.
- `src/WriterXML.py`: converte tokens em XML e grava em arquivo.
- `src/utils.py`: utilitarios de leitura de arquivo.
- `tests/inputs/`: programas Jack de entrada para teste.
- `tests/expected/`: saidas XML esperadas para comparacao.
- `output/`: saidas geradas pelo tokenizer.

## Observacoes
O projeto nao usa ferramentas automaticas como Lex, Flex ou Yacc, priorizando a implementacao manual dos conceitos de compiladores.
