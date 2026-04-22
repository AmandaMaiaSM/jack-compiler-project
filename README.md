# jack-compiler-project
### Jack Compiler

## Descricao
Este projeto implementa um compilador para a linguagem Jack (Nand2Tetris), com foco inicial na etapa de analise lexica. O tokenizer le arquivos `.jack`, remove comentarios, valida delimitadores e gera tokens que sao exportados em XML.

## Integrantes
- Amanda Maia Soares Silva
- Marcos Antonio Branco Pereira Junior

## Linguagem utilizada
Python

## Etapas do projeto
1. Analisador Lexico (Tokenizer) - etapa atual
2. Analisador Sintatico (Parser)
3. Geracao de Codigo (VM)

## Como rodar
1. Escolha o arquivo de entrada em `main.py` (ex.: `tests\inputs\Main.jack`).
2. Execute:

```bash
python main.py
```

O XML de tokens e salvo em `output/` com o sufixo `T.xml`.

## Arquitetura (fluxo de execucao)
1. `main.py` instancia o `Scanner` e aponta o arquivo `.jack` de entrada.
2. `Scanner.tokenizar()` le o arquivo, pede ao `Tokenizer` para extrair tokens brutos, remove comentarios e valida blocos.
3. `Tokenizer.classificar_tokens()` transforma tokens brutos em instancias de `Token` com tipo, valor e linha.
4. `WriterXML` converte os tokens para XML e grava o arquivo de saida.

## Estrutura de pastas
```
jack-compiler-project/
	main.py
	README.md
	output/                 # saidas geradas (XML)
	src/
		scanner/
			Scanner.py          # orquestra a etapa lexica
			Tokenizer.py        # extrai, filtra e classifica tokens
			Token.py            # modelo de token (tipo, valor, linha)
			WriterXML.py        # gera o XML de tokens
			utils.py            # utilitarios de IO (ex.: leitura de arquivo)
	tests/
		inputs/               # entradas Jack de exemplo
		expected/             # saidas XML esperadas
```

## Descricao dos arquivos
- `main.py`: ponto de entrada que executa o tokenizer e imprime o XML.
- `src/scanner/Scanner.py`: orquestra leitura, tokenizacao, validacao e escrita do XML.
- `src/scanner/Tokenizer.py`: implementa a analise lexica (tokenizacao, remocao de comentarios e validacao de blocos).
- `src/scanner/Token.py`: classe `Token` para representar tipo, valor e linha.
- `src/scanner/WriterXML.py`: converte tokens em XML e grava em arquivo.
- `src/scanner/utils.py`: utilitarios de leitura de arquivo.
- `tests/inputs/`: programas Jack de entrada para teste.
- `tests/expected/`: saidas XML esperadas para comparacao.
- `output/`: saidas geradas pelo tokenizer.

## Observacoes
O projeto nao usa ferramentas automaticas como Lex, Flex ou Yacc, priorizando a implementacao manual dos conceitos de compiladores.
