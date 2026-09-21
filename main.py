"""Exibe a amostra ampliada da KaBuM e salva os dados brutos em CSV."""

from pathlib import Path

import pandas as pd

from scraper import coletar_produtos as coletar_kabum


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
    print(f"Páginas consultadas: {resumo['paginas']}")
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
    exibir_produtos(kabum)

    print("=" * 40)
    print("RESUMO DA COLETA")
    exibir_resumo("KaBuM", kabum, resumo_kabum)
    produtos = kabum
    print(f"\nTotal coletado: {len(produtos)} registros")
    if not produtos:
        print("Nenhuma oferta válida. O CSV anterior foi preservado; nenhum arquivo foi gravado.")
        return 1
    try:
        salvar_csv(produtos)
    except OSError as erro:
        print(f"Não foi possível salvar o CSV: {erro}")
        return 1

    print(f"Total salvo no CSV: {len(produtos)} registros.")
    print(f"Arquivo salvo em {ARQUIVO_CSV}")
    if len(produtos) < 60:
        print("Aviso: a coleta ficou abaixo da meta de 60 a 100 ofertas.")
    print("=" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
