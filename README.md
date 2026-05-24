# Jack Compiler — Nand2Tetris (Project 11)

Compilador completo da linguagem **Jack** para código da máquina virtual (`.vm`), implementado em Python.  
Cobre as etapas de análise léxica, análise sintática e geração de código intermediário.

---

## Integrantes

| Nome | Matrícula |
|------|-----------|
| Amanda Maia Soares Silva | *preencher* |
| Marcos Antonio Branco Pereira Junior | *preencher* |

---

## Linguagem utilizada

Python 3.12

---

## Como compilar e executar

### Compilar um arquivo único

```bash
python main.py input/Seven/Main.jack
```

### Compilar um diretório inteiro

```bash
python main.py input/Square/
python main.py input/Pong/
```

O compilador identifica todos os arquivos `.jack` no diretório e gera um `.vm` para cada um, no mesmo local.

### Modo debug (gera XML do scanner e parser)

```bash
python main.py --xml input/Square/Main.jack
```

---

## Estrutura do projeto

```
jack-compiler-project/
  main.py                   # ponto de entrada
  README.md
  input/                    # programas Jack de referência (Project 11)
    Seven/
    Average/
    ConvertToBin/
    ComplexArrays/
    Square/
    Pong/
  output/                   # XMLs gerados no modo --xml
  expected/                 # XMLs de referência para comparação
  src/
    scanner/
      Scanner.py            # orquestração da análise léxica
      Tokenizer.py          # extração e classificação de tokens
      Token.py              # modelo de token (tipo, valor)
      utils.py              # leitura de arquivo
    parser/
      Parser.py             # consumo de tokens e utilitários
      Grammar.py            # regras gramaticais (parse_*)
    codegen/
      CodeGenerator.py      # geração de código VM (parsing + emissão em passagem única)
      SymbolTable.py        # tabela de símbolos (escopo de classe e subrotina)
      VMWriter.py           # escrita das instruções VM no arquivo de saída
      tests/
        test_vm_writer.py   # testes unitários do VMWriter
        test_symbol_table.py# testes unitários da SymbolTable
        test_codegen.py     # testes de integração + validação dos programas do Project 11
        inputs/             # snippets Jack focados por funcionalidade
        expected/           # saídas VM de referência para os snippets
    utils/
      WriterXML.py          # escrita e comparação de arquivos XML
```

---

## Executando os testes

```bash
# instalar pytest (primeira vez)
python -m pip install pytest

# rodar todos os testes
python -m pytest src/codegen/tests/ -v
```

**Resultado esperado:** 80 testes passando.

---

## Status da validação — Project 11

| Programa | Arquivos `.jack` | Compilado | Validado no VM Emulator |
|----------|-----------------|-----------|------------------------|
| Seven | `Main.jack` | ✅ | ✅ |
| Average | `Main.jack` | ✅ | ✅ |
| ConvertToBin | `Main.jack` | ✅ | ✅ |
| ComplexArrays | `Main.jack` | ✅ | ✅ |
| Square | `Main.jack`, `Square.jack`, `SquareGame.jack` | ✅ | ✅ |
| Pong | `Main.jack`, `Ball.jack`, `Bat.jack`, `PongGame.jack` | ✅ | ✅ |

---

## Desafios enfrentados

**Atribuição a arrays (`let arr[i] = expr`):**  
O maior cuidado foi garantir a ordem correta das operações na pilha. O endereço de destino (`arr + i`) precisa ser calculado *antes* da expressão do lado direito, mas o ponteiro `THAT` só pode ser definido *depois* — exigindo salvar o valor em `temp 0`, ajustar o ponteiro e então gravar via `that 0`.

**Distinção entre chamada de método e função estática:**  
Ao compilar `nome.metodo()`, o compilador precisa consultar a tabela de símbolos: se `nome` é uma variável de objeto, empurra ela como primeiro argumento (`this`) e usa o tipo da variável como nome da classe; se `nome` é um identificador de classe (não existe na tabela), é uma chamada estática direta.

**Compilação em lote de diretórios:**  
A tabela de símbolos precisa ser limpa entre classes (o escopo de `static` e `field` é por classe). Como o `CodeGenerator` é instanciado uma vez por arquivo, isso é garantido naturalmente — cada arquivo gera um novo `CodeGenerator` com uma `SymbolTable` zerada.
