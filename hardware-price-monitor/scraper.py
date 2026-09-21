"""Etapa 1: coleta de ofertas RTX série 50 vendidas pela própria KaBuM."""

import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL_BASE = "https://www.kabum.com.br"
URL_BUSCA = f"{URL_BASE}/busca/rtx-50"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Seletor confirmado no HTML real. Os cartões visuais são placeholders.
SELETOR_DADOS = 'script#__NEXT_DATA__[type="application/json"]'
# Caminho dos produtos: props.pageProps.data.catalogServer.data
# Nome: name | Preço à vista: priceWithDiscount
# URL: /produto/{code}/{friendlyName}, conforme as URLs do script#productSchema.
# Paginação: props.pageProps.data.catalogServer.pagination.next
# Não há seletores de nome/preço nos cartões do HTML recebido por requests.
PADRAO_RTX_50 = re.compile(r"\bRTX\s*50\d{2}(?:\s*Ti)?\b", re.IGNORECASE)


def ler_catalogo(html):
    """Lê os dados incorporados ao HTML, sem executar JavaScript."""
    pagina = BeautifulSoup(html, "html.parser")
    bloco = pagina.select_one(SELETOR_DADOS)
    if bloco is None:
        raise ValueError("Bloco __NEXT_DATA__ ausente: possível bloqueio ou mudança do site.")
    try:
        # Preserva a representação decimal original, sem normalizar os preços.
        dados = json.loads(bloco.get_text(), parse_float=str)
        catalogo = dados["props"]["pageProps"]["data"]["catalogServer"]
        produtos = catalogo["data"]
        proxima = catalogo["pagination"]["next"]
        if not isinstance(produtos, list) or not isinstance(proxima, int):
            raise ValueError("Formato inesperado do catálogo ou da paginação.")
    except (KeyError, TypeError, json.JSONDecodeError) as erro:
        raise ValueError("Estrutura do catálogo da KaBuM não reconhecida.") from erro
    return produtos, proxima


def extrair_produto(item):
    """Seleciona ofertas do escopo sem limpar ou transformar os valores."""
    if not isinstance(item, dict):
        return None, "incompletos"

    nome = item.get("name")
    categoria = item.get("category")
    vendedor = item.get("sellerName")
    if not all(isinstance(campo, str) and campo.strip() for campo in (nome, categoria, vendedor)):
        return None, "incompletos"

    # A busca também retorna notebooks, outras GPUs e vendedores de marketplace.
    if (
        not PADRAO_RTX_50.search(nome)
        or "Placa de vídeo (VGA)" not in categoria
        or vendedor != "KaBuM!"
    ):
        return None, "fora_escopo"
    if item.get("available") is not True:
        return None, "indisponiveis"

    preco = item.get("priceWithDiscount")
    codigo = item.get("code")
    slug = item.get("friendlyName")
    # Verificação mínima; mantém o preço como veio do JSON (ex.: "2799.99").
    preco_texto = str(preco)
    if (
        not re.fullmatch(r"\d+(?:\.\d+)?", preco_texto)
        or not preco_texto.replace(".", "").strip("0")
        or not isinstance(codigo, int)
        or isinstance(codigo, bool)
        or codigo <= 0
        or not isinstance(slug, str)
        or not slug.strip()
    ):
        return None, "incompletos"

    return {
        "nome_produto": nome,
        "preco": preco,
        "loja": "KaBuM",
        "url": urljoin(URL_BASE, f"/produto/{codigo}/{slug}"),
        "categoria": "Placa de vídeo",
    }, None


def coletar_produtos(limite=30, max_paginas=5):
    produtos = []
    urls_vistas = set()
    resumo = dict(encontrados=0, incompletos=0, fora_escopo=0, indisponiveis=0, repetidos=0)
    pagina = 1

    with requests.Session() as sessao:
        sessao.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"})
        for _ in range(max_paginas):
            print(f"Consultando {URL_BUSCA} — página {pagina}...")
            try:
                resposta = sessao.get(
                    URL_BUSCA,
                    params={"page_number": pagina, "page_size": 60},
                    timeout=30,
                )
                resposta.raise_for_status()
                itens, proxima = ler_catalogo(resposta.text)
            except (requests.RequestException, ValueError) as erro:
                print(f"Aviso: não foi possível coletar a página {pagina}: {erro}")
                break

            for item in itens:
                resumo["encontrados"] += 1
                produto, motivo = extrair_produto(item)
                if motivo:
                    resumo[motivo] += 1
                    continue
                if produto["url"] in urls_vistas:
                    resumo["repetidos"] += 1
                    continue
                urls_vistas.add(produto["url"])
                produtos.append(produto)
                if len(produtos) >= limite:
                    return produtos, resumo

            if not itens or proxima <= pagina:
                break
            pagina = proxima
            time.sleep(1)

    return produtos, resumo
