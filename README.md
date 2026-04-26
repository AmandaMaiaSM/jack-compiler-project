# jack-compiler-project
### Jack Compiler (Nand2Tetris)

## Descrição
Este projeto implementa as etapas iniciais de um compilador para a linguagem Jack:
1. Análise léxica (tokenizer/scanner)
2. Análise sintática (parser)

O programa lê arquivos `.jack`, gera os tokens em XML e também gera a árvore sintática em XML.

## Integrantes
- Amanda Maia Soares Silva
- Marcos Antonio Branco Pereira Junior

## Linguagem utilizada
Python

## Status das etapas
1. Analisador Léxico (Tokenizer): concluído
2. Analisador Sintático (Parser + Grammar): concluído
3. Geração de Código VM: pendente

## Como rodar
1. Defina o arquivo de entrada em `main.py` (exemplo: `input/Main.jack`).
2. Execute:

```bash
python main.py
```

## Saídas geradas
Para cada arquivo `.jack` processado:
- `output/<Nome>T.xml`: lista de tokens
- `output/<Nome>P.xml`: árvore sintática (parse tree)

Exemplo para `input/Main.jack`:
- `output/MainT.xml`
- `output/MainP.xml`

## Fluxo de execução
1. `main.py` cria o `Scanner`, tokeniza o arquivo e coleta os tokens.
2. `WriterXML` escreve os tokens em `output/<Nome>T.xml`.
3. `Parser` recebe os tokens e gera o XML da árvore sintática.
4. `WriterXML` escreve o parser em `output/<Nome>P.xml`.
5. O método `WriterXML.comparar_arquivos(arquivo1, arquivo2)` pode ser usado para comparar a saída gerada com o arquivo de referência em `expected/<Nome>.xml`.

## Estrutura de pastas (resumo)
```text
jack-compiler-project/
  main.py
  README.md
  input/                  # arquivos .jack de entrada
  output/                 # XMLs gerados (T.xml e P.xml)
  expected/               # XMLs de referência (parser) para comparação
  src/
    scanner/
      Scanner.py          # orquestração da etapa léxica
      Tokenizer.py        # extração e classificação de tokens
      Token.py            # modelo de token (tipo, valor, linha)
      utils.py            # leitura de arquivo
    parser/
      Parser.py           # estado do parser + utilitários de tokens/XML
      Grammar.py          # regras gramaticais (parse_*)
    utils/
      WriterXML.py        # escrita/comparação dos arquivos XML
```

## Observações
- A implementação é manual, sem uso de Lex/Flex/Yacc.
- O parser atual foi refatorado para separar regras gramaticais em `Grammar.py` e manter o `Parser.py` como coordenador da análise.

## Comparação de arquivos de saída
Para comparar a saída gerada (`output/<Nome>P.xml`) com um arquivo de referência (`expected/<Nome>.xml`), utilize:

```python
from src.utils.WriterXML import WriterXML

WriterXML.comparar_arquivos("output/MainP.xml", "expected/Main.xml")
```

Se os arquivos forem iguais, o método retorna `True` e imprime `Os arquivos são iguais.`. Caso contrário, retorna `False` e imprime `Os arquivos são diferentes.`.
