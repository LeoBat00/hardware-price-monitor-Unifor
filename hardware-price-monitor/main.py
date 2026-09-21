"""Exibe a coleta da KaBuM e salva os dados brutos em CSV."""

from pathlib import Path

import pandas as pd

from scraper import coletar_produtos


ARQUIVO_CSV = Path(__file__).resolve().parent / "data" / "dados_brutos.csv"
COLUNAS = ["nome_produto", "preco", "loja", "url", "categoria"]


def exibir_produtos(produtos):
    print(f"\nProdutos válidos encontrados: {len(produtos)}\n")
    for numero, produto in enumerate(produtos, start=1):
        print(f"[{numero}]")
        print(f"Produto: {produto['nome_produto']}")
        print(f"Preço (BRL, à vista, valor bruto): {produto['preco']}")
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


def main():
    print("=" * 40)
    print("MONITORAMENTO DE PREÇOS - KABUM")
    print("=" * 40)
    produtos, resumo = coletar_produtos()
    exibir_produtos(produtos)

    print("=" * 40)
    print(f"Quantidade encontrada e examinada até o limite: {resumo['encontrados']}")
    print(f"Quantidade válida: {len(produtos)}")
    print(f"Ignorada por erro/informação ausente: {resumo['incompletos']}")
    print(f"Fora do escopo (modelo/categoria/vendedor): {resumo['fora_escopo']}")
    print(f"Indisponível: {resumo['indisponiveis']}")
    print(f"Repetida entre páginas: {resumo['repetidos']}")
    if not produtos:
        print("Nenhuma oferta válida coletada. O CSV não foi criado nem substituído.")
        return 1
    try:
        salvar_csv(produtos)
    except OSError as erro:
        print(f"Não foi possível salvar o CSV: {erro}")
        return 1

    print(f"{len(produtos)} produtos coletados.")
    print(f"Arquivo salvo em {ARQUIVO_CSV}")
    if len(produtos) < 20:
        print("Aviso: a coleta ficou abaixo da meta de 20 a 30 ofertas.")
    print("=" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
