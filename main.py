"""Exibe as coletas da KaBuM e Amazon e salva um CSV bruto combinado."""

from pathlib import Path

import pandas as pd

from scraper import coletar_produtos as coletar_kabum
from scraper_amazon import coletar_produtos as coletar_amazon


ARQUIVO_CSV = Path(__file__).resolve().parent / "data" / "dados_brutos.csv"
COLUNAS = ["nome_produto", "preco", "loja", "url", "categoria"]


def exibir_produtos(produtos):
    print(f"\nProdutos válidos encontrados: {len(produtos)}\n")
    for numero, produto in enumerate(produtos, start=1):
        print(f"[{numero}]")
        print(f"Produto: {produto['nome_produto']}")
        print(f"Preço (BRL, valor bruto da oferta): {produto['preco']}")
        print(f"Loja: {produto['loja']}")
        print(f"Categoria: {produto['categoria']}")
        print(f"URL: {produto['url']}")
        print("-" * 40)


def salvar_csv(produtos):
    ARQUIVO_CSV.parent.mkdir(parents=True, exist_ok=True)
    # dtype=object evita que o pandas converta os valores antes de gravá-los.
    pd.DataFrame(produtos, columns=COLUNAS, dtype=object).to_csv(
        ARQUIVO_CSV, index=False, encoding="utf-8-sig"
    )


def exibir_resumo(loja, produtos, resumo):
    print(f"\n{loja}: {len(produtos)} ofertas válidas")
    print(f"Registros examinados até o limite: {resumo['encontrados']}")
    print(f"Ignorados por erro/informação ausente: {resumo['incompletos']}")
    print(f"Fora do escopo: {resumo['fora_escopo']}")
    if "indisponiveis" in resumo:
        print(f"Indisponíveis: {resumo['indisponiveis']}")
    print(f"Repetidos durante a coleta: {resumo['repetidos']}")


def main():
    print("=" * 40)
    print("MONITORAMENTO DE PREÇOS")
    print("=" * 40)
    print("\nColetando KaBuM...")
    kabum, resumo_kabum = coletar_kabum()
    print(f"{len(kabum)} ofertas válidas.")
    print("\nColetando Amazon...")
    amazon, resumo_amazon = coletar_amazon()
    print(f"{len(amazon)} ofertas válidas.")

    for loja, ofertas in (("KABUM", kabum), ("AMAZON", amazon)):
        print("\n" + "=" * 40)
        print(loja)
        print("=" * 40)
        exibir_produtos(ofertas)

    print("=" * 40)
    print("RESUMO DA COLETA")
    exibir_resumo("KaBuM", kabum, resumo_kabum)
    exibir_resumo("Amazon", amazon, resumo_amazon)
    produtos = kabum + amazon
    print(f"\nTotal coletado: {len(produtos)} registros")
    if not kabum or not amazon or resumo_amazon.get("erro"):
        print("Coleta combinada incompleta. O CSV anterior foi preservado; nenhum arquivo foi gravado.")
        return 1
    try:
        salvar_csv(produtos)
    except OSError as erro:
        print(f"Não foi possível salvar o CSV: {erro}")
        return 1

    print(f"{len(produtos)} produtos coletados.")
    print(f"Arquivo salvo em {ARQUIVO_CSV}")
    for loja, ofertas in (("KaBuM", kabum), ("Amazon", amazon)):
        if len(ofertas) < 20:
            print(f"Aviso: {loja} ficou abaixo da meta de 20 a 30 ofertas.")
    print("=" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
