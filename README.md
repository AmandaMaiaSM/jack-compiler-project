# jack-compiler-project
### Jack Compiler (Nand2Tetris)

## Descricao
Este projeto implementa as etapas iniciais de um compilador para a linguagem Jack:
1. analise lexica (tokenizer/scanner)
2. analise sintatica (parser)

O programa le arquivos `.jack`, gera os tokens em XML e tambem gera a arvore sintatica em XML.

## Integrantes
- Amanda Maia Soares Silva
- Marcos Antonio Branco Pereira Junior

## Linguagem utilizada
Python

## Status das etapas
1. Analisador Lexico (Tokenizer): concluido
2. Analisador Sintatico (Parser + Grammar): concluido
3. Geracao de Codigo VM: pendente

## Como rodar
1. Defina o arquivo de entrada em `main.py` (exemplo: `input/Main.jack`).
2. Execute:

```bash
python main.py
```

## Saidas geradas
Para cada arquivo `.jack` processado:
- `output/<Nome>T.xml`: lista de tokens
- `output/<Nome>P.xml`: arvore sintatica (parse tree)

Exemplo para `input/Main.jack`:
- `output/MainT.xml`
- `output/MainP.xml`

## Fluxo de execucao
1. `main.py` cria o `Scanner`, tokeniza o arquivo e coleta os tokens.
2. `Parser` recebe os tokens.
3. `Grammar` aplica as regras sintaticas da linguagem Jack.
4. `WriterXML` escreve os XMLs de tokens (`T.xml`) e parser (`P.xml`).

## Estrutura de pastas (resumo)
```text
jack-compiler-project/
  main.py
  README.md
  input/                  # arquivos .jack de entrada
  output/                 # XMLs gerados (T.xml e P.xml)
  src/
    scanner/
      Scanner.py          # orquestracao da etapa lexica
      Tokenizer.py        # extracao e classificacao de tokens
      Token.py            # modelo de token (tipo, valor, linha)
      utils.py            # leitura de arquivo
    parser/
      Parser.py           # estado do parser + utilitarios de tokens/XML
      Grammar.py          # regras gramaticais (parse_*)
    utils/
      WriterXML.py        # escrita dos arquivos XML
```

## Observacoes
- A implementacao e manual, sem uso de Lex/Flex/Yacc.
- O parser atual foi refatorado para separar regras gramaticais em `Grammar.py` e manter o `Parser.py` como coordenador da analise.
