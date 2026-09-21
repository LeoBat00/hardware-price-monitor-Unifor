"""Coleta pequena de placas de vídeo na busca pública da Amazon Brasil."""

import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


URL_BASE = "https://www.amazon.com.br"
URL_BUSCA = f"{URL_BASE}/s?k=placa+de+video+RTX"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Seletores confirmados na resposta HTTP 200 da busca, antes da implementação.
SELETOR_PRODUTO = 'div[data-component-type="s-search-result"]'
SELETOR_NOME = '[data-cy="title-recipe"] h2'
SELETOR_URL = '[data-cy="title-recipe"] a[href]'
# Primeiro preço principal do cartão; exclui preço riscado e parcelas menores.
# Pode ser Pix/NuPay ou preço normal, conforme a oferta. Preserva inclusive NBSP.
SELETOR_PRECO = '[data-cy="price-recipe"] .a-price:not(.a-text-price) .a-offscreen'
SELETOR_PROXIMA = 'a.s-pagination-next[href]'
# data-asin identifica o produto e evita repetições com links de rastreamento distintos.
# "Amazon" identifica a fonte: a busca também oferece produtos de terceiros.

PADRAO_PLACA = re.compile(
    r"placa\s+(?:de\s+v[ií]deo|gr[aá]fica)|\bgpu\b|\bgeforce\b|\brtx\s*\d{4}",
    re.IGNORECASE,
)
PADRAO_FORA_ESCOPO = re.compile(
    r"\b(?:notebook|laptop|computador|desktop|pc\s+gamer|mini\s*pc|"
    r"cabo|suporte|adaptador|extensor|riser|cooler|ventoinha|waterblock|"
    r"processador|placa\s+m[aã]e)\b",
    re.IGNORECASE,
)


def url_amazon(url):
    endereco = urlparse(url)
    return endereco.scheme == "https" and endereco.netloc == "www.amazon.com.br"


def ler_pagina(html):
    pagina = BeautifulSoup(html, "html.parser")
    titulo = pagina.title.get_text().lower() if pagina.title else ""
    texto = pagina.get_text(" ", strip=True).lower()
    formularios = " ".join(str(f.get("action", "")) for f in pagina.find_all("form"))
    # Interrompe a coleta diante de proteção; não tenta resolver desafios.
    if (
        "captcha" in formularios.lower()
        or any(t in titulo for t in ("robot check", "captcha", "just a moment", "verificação", "sign-in"))
        or "digite os caracteres que você vê" in texto
        or "enter the characters you see" in texto
        or "sorry, we just need to make sure you're not a robot" in texto
    ):
        raise ValueError("Página de verificação/autenticação recebida. Coleta interrompida.")

    itens = pagina.select(SELETOR_PRODUTO)
    if not itens:
        raise ValueError("Nenhum cartão de produto no HTML: busca vazia, bloqueio ou mudança de estrutura.")
    proxima = pagina.select_one(SELETOR_PROXIMA)
    return itens, urljoin(URL_BASE, proxima["href"]) if proxima else None


def extrair_produto(item):
    nome_tag = item.select_one(SELETOR_NOME)
    preco_tag = item.select_one(SELETOR_PRECO)
    link = item.select_one(SELETOR_URL)
    asin = item.get("data-asin", "")
    if nome_tag is None:
        return None, "incompletos"
    nome = nome_tag.get_text()
    if not nome.strip():
        return None, "incompletos"
    if not PADRAO_PLACA.search(nome) or PADRAO_FORA_ESCOPO.search(nome):
        return None, "fora_escopo"
    if preco_tag is None or link is None or not re.fullmatch(r"[A-Z0-9]{10}", asin):
        return None, "incompletos"

    preco = preco_tag.get_text()
    url = urljoin(URL_BASE, link["href"])
    if (
        not preco.strip()
        or not any(c.isdigit() for c in preco)
        or not url_amazon(url)
        or f"/dp/{asin}" not in urlparse(url).path
    ):
        return None, "incompletos"
    return {
        "nome_produto": nome,
        "preco": preco,
        "loja": "Amazon",
        "url": url,
        "categoria": "Placa de vídeo",
    }, None


def coletar_produtos(limite=30, max_paginas=3):
    produtos = []
    asins_vistos = set()
    paginas_vistas = set()
    resumo = dict(encontrados=0, incompletos=0, fora_escopo=0, repetidos=0, erro=None)
    url = URL_BUSCA
    with requests.Session() as sessao:
        sessao.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"})
        for numero in range(1, max_paginas + 1):
            if not url or url in paginas_vistas:
                break
            if not url_amazon(url):
                resumo["erro"] = "Link de paginação fora do domínio esperado. Coleta interrompida."
                print(f"Aviso Amazon: {resumo['erro']}")
                break
            paginas_vistas.add(url)
            print(f"Consultando Amazon — página {numero}...")
            try:
                resposta = sessao.get(url, timeout=30)
                print(f"Amazon: HTTP {resposta.status_code}")
                resposta.raise_for_status()
                itens, proxima = ler_pagina(resposta.text)
            except (requests.RequestException, ValueError) as erro:
                resumo["erro"] = str(erro)
                print(f"Aviso Amazon: {erro}")
                break

            for item in itens:
                resumo["encontrados"] += 1
                produto, motivo = extrair_produto(item)
                if motivo:
                    resumo[motivo] += 1
                    continue
                asin = item["data-asin"]
                if asin in asins_vistos:
                    resumo["repetidos"] += 1
                    continue
                asins_vistos.add(asin)
                produtos.append(produto)
                if len(produtos) >= limite:
                    return produtos, resumo
            url = proxima
            if url and numero < max_paginas:
                time.sleep(1)
    return produtos, resumo
