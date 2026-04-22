import os
from src.scanner.utils import read_file
from src.scanner.Tokenizer import Tokenizer
from src.utils.WriterXML import WriterXML


class Scanner:

    def __init__(self, arquivo_entrada):
        self.arquivo_entrada = arquivo_entrada
        self.tokenizer = Tokenizer()
        self.writer_xml = WriterXML()
        self.tokens_classificados = []

    def tokenizar(self, caminho_saida=None):
        codigo = read_file(self.arquivo_entrada)

        tokens = self.tokenizer.extrair_tokens_brutos(codigo)

        tokens_sem_comentarios = self.tokenizer.remover_comentarios(tokens)

        self.tokenizer.validar_blocos(tokens_sem_comentarios)

        self.tokens_classificados = self.tokenizer.classificar_tokens(
            tokens_sem_comentarios
        )

        if caminho_saida is None:
            caminho_saida = self._gerar_caminho_saida()

        xml_texto = self.writer_xml.escrever_tokens(
            self.tokens_classificados, caminho_saida
        )

        return xml_texto

    def _gerar_caminho_saida(self):
        nome_base = os.path.splitext(os.path.basename(self.arquivo_entrada))[0]
        return os.path.join("output", f"{nome_base}T.xml")

    def get_tokens(self):
        return self.tokens_classificados
