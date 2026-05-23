import os
import sys

from src.scanner.Scanner import Scanner
from src.parser.Parser import Parser
from src.utils.WriterXML import WriterXML
from src.codegen.CodeGenerator import CodeGenerator


def compile_vm(jack_path):
    output_vm = os.path.splitext(jack_path)[0] + '.vm'
    scanner = Scanner(jack_path)
    scanner.tokenizar()
    tokens = scanner.get_tokens()
    gen = CodeGenerator(tokens, output_vm)
    gen.compile()
    print(f'Gerado: {output_vm}')


def compile_xml(jack_path):
    scanner = Scanner(jack_path)
    scanner.tokenizar()
    tokens = scanner.get_tokens()
    nome_base = os.path.splitext(os.path.basename(jack_path))[0]
    WriterXML().escrever_tokens(tokens, os.path.join('output', f'{nome_base}T.xml'))
    xml_output = Parser(tokens).parse()
    arquivo_saida = os.path.join('output', f'{nome_base}P.xml')
    WriterXML().escrever_parser(xml_output, arquivo_saida)
    arquivo_esperado = os.path.join('expected', f'{nome_base}.xml')
    resultado = WriterXML.comparar_arquivos(arquivo_saida, arquivo_esperado)
    print(f'XML {nome_base}: {"iguais" if resultado else "diferentes"}')


def collect_jack_files(path):
    if os.path.isfile(path) and path.endswith('.jack'):
        return [path]
    files = []
    for root, _, names in os.walk(path):
        for name in names:
            if name.endswith('.jack'):
                files.append(os.path.join(root, name))
    return sorted(files)


def main():
    args = sys.argv[1:]
    xml_mode = '--xml' in args
    paths = [a for a in args if not a.startswith('--')]

    if not paths:
        print('Uso: python main.py [--xml] <arquivo.jack ou diretório>')
        print('  --xml   gera XML de tokens e árvore sintática (modo debug)')
        print('Exemplos:')
        print('  python main.py input/Seven/')
        print('  python main.py input/Square/Main.jack')
        print('  python main.py --xml input/Main.jack')
        sys.exit(0)

    jack_files = []
    for p in paths:
        jack_files.extend(collect_jack_files(p))

    if not jack_files:
        print('Nenhum arquivo .jack encontrado.')
        sys.exit(1)

    for jack_path in jack_files:
        if xml_mode:
            compile_xml(jack_path)
        else:
            compile_vm(jack_path)


if __name__ == '__main__':
    main()
