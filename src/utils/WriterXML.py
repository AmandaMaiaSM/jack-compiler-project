import os
from xml.sax.saxutils import escape


class WriterXML:
	def __init__(self):
		self._mapa_tipos = {
			"keyword": "keyword",
			"symbol": "symbol",
			"identifier": "identifier",
			"integerconstant": "integerConstant",
			"stringconstant": "stringConstant",
			"int_const": "integerConstant",
			"string_const": "stringConstant",
		}

	def _nome_tag(self, token_type):
		valor = getattr(token_type, "value", token_type)
		chave = str(valor).lower()
		return self._mapa_tipos.get(chave, chave)

	def tokens_para_xml(self, tokens):
		linhas = ["<tokens>"]
		for token in tokens:
			tag = self._nome_tag(token.type)
			valor = escape(str(token.value), {'"': "&quot;"})
			linhas.append(f"<{tag}> {valor} </{tag}>")
		linhas.append("</tokens>")
		return "\n".join(linhas)

	def escrever_tokens(self, tokens, caminho_saida):
		xml_texto = self.tokens_para_xml(tokens)
		pasta_saida = os.path.dirname(caminho_saida)
		if pasta_saida:
			os.makedirs(pasta_saida, exist_ok=True)
		with open(caminho_saida, "w", encoding="utf-8") as arquivo:
			arquivo.write(xml_texto + "\n")
		return xml_texto
	
	def escrever_parser(self, xml_texto, caminho_saida):
		pasta_saida = os.path.dirname(caminho_saida)
		if pasta_saida:
			os.makedirs(pasta_saida, exist_ok=True)
		with open(caminho_saida, "w", encoding="utf-8") as arquivo:
			arquivo.write(xml_texto + "\n")

	@staticmethod
	def comparar_arquivos(arquivo1, arquivo2):
		with open(arquivo1, 'r', encoding='utf-8') as f1, open(arquivo2, 'r', encoding='utf-8') as f2:
			conteudo1 = f1.read()
			conteudo2 = f2.read()
			if conteudo1 == conteudo2:
				print("Os arquivos são iguais.")
				return True
			else:
				print("Os arquivos são diferentes.")
				return False
