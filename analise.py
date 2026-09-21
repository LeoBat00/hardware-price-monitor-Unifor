"""Análise local da amostra tratada; não coleta nem modifica os CSVs."""

import hashlib
import json
import math
from pathlib import Path

import pandas as pd


PASTA_DADOS = Path(__file__).resolve().parent / "data"
ARQUIVO_ENTRADA = PASTA_DADOS / "dados_tratados.csv"
ARQUIVO_RESULTADOS = PASTA_DADOS / "resultados_analise.json"
COLUNAS = ["nome_produto", "preco", "loja", "url", "categoria", "fabricante", "modelo_gpu", "familia_gpu"]
# Cortes definidos após observar a base: R$ 1.349,99 a R$ 15.999,99.
# Intervalos abertos à esquerda e fechados à direita; extremos cobrem a base.
LIMITES_FAIXAS = [0, 1500, 3000, 5000, 8000, 12000, math.inf]


def moeda(valor):
    if valor is None:
        return "Não calculável"
    return "R$ " + f"{valor:,.2f}".translate(str.maketrans({",": ".", ".": ","}))


def validar_base(dados):
    if set(COLUNAS) - set(dados.columns):
        raise ValueError("A base deve conter as oito colunas da etapa 4.")
    if dados.empty:
        raise ValueError("A base tratada está vazia.")
    if dados[COLUNAS].isna().any().any():
        raise ValueError("Há campos ausentes. Revise o pré-processamento.")
    for coluna in COLUNAS:
        if coluna != "preco" and dados[coluna].astype(str).str.strip().eq("").any():
            raise ValueError(f"Há valores vazios em {coluna}.")
    if (
        not pd.api.types.is_numeric_dtype(dados.preco)
        or pd.api.types.is_bool_dtype(dados.preco)
        or not dados.preco.map(math.isfinite).all()
        or not dados.preco.gt(0).all()
    ):
        raise ValueError("A coluna preco deve ser numérica, finita e positiva.")
    if dados.url.duplicated().any():
        raise ValueError("Há URLs duplicadas. Revise o pré-processamento.")
    if set(dados.loja) != {"KaBuM"}:
        raise ValueError("Esta análise se refere exclusivamente à amostra da KaBuM.")


def agrupar(dados, coluna, amplitude=False):
    grupos = dados.groupby(coluna, sort=True).preco.agg(
        quantidade="count", preco_medio="mean", mediana="median",
        preco_minimo="min", preco_maximo="max",
    ).reset_index()
    if amplitude:
        grupos["amplitude"] = grupos.preco_maximo - grupos.preco_minimo
        grupos["amplitude_percentual"] = grupos.amplitude / grupos.preco_minimo * 100
        grupos["multiplas_ofertas"] = grupos.quantidade.ge(2)
    return grupos.sort_values(["quantidade", coluna], ascending=[False, True]).to_dict("records")


def distribuir_faixas(precos):
    faixas = []
    for inferior, superior in zip(LIMITES_FAIXAS, LIMITES_FAIXAS[1:]):
        quantidade = int(((precos > inferior) & (precos <= superior)).sum())
        if inferior == 0:
            nome = f"Até {moeda(superior)}"
        elif math.isinf(superior):
            nome = f"Acima de {moeda(inferior)}"
        else:
            nome = f"Acima de {moeda(inferior)} até {moeda(superior)}"
        faixas.append({
            "faixa": nome, "limite_inferior_exclusivo": inferior,
            "limite_superior_inclusivo": None if math.isinf(superior) else superior,
            "quantidade": quantidade, "percentual": quantidade / len(precos) * 100,
        })
    return faixas


def gerar_insights(resultado):
    total = resultado["resumo"]["quantidade"]
    faixa = max(resultado["faixas_preco"], key=lambda f: f["quantidade"])
    insights = [
        f"Na amostra da KaBuM, a faixa '{faixa['faixa']}' reúne "
        f"{faixa['quantidade']} de {total} ofertas ({faixa['percentual']:.2f}%)."
    ]
    modelos = resultado["destaques_modelos"]["maiores_amplitudes"]
    if modelos:
        m = modelos[0]
        insights.append(
            f"Entre os modelos com pelo menos duas ofertas, {m['modelo_gpu']} apresenta "
            f"a maior amplitude: {moeda(m['amplitude'])}, de {moeda(m['preco_minimo'])} "
            f"a {moeda(m['preco_maximo'])}, em {m['quantidade']} ofertas "
            f"({m['amplitude_percentual']:.2f}% do menor preço). As placas podem diferir "
            "em memória, construção e outras especificações não controladas."
        )
    familia = resultado["por_familia"][0]
    insights.append(
        f"A família {familia['familia_gpu']} reúne {familia['quantidade']} de {total} "
        f"ofertas ({familia['quantidade'] / total * 100:.2f}%), com mediana de "
        f"{moeda(familia['mediana'])}. Essa composição da amostra deve ser considerada "
        "ao interpretar a distribuição geral; não mede participação no mercado."
    )
    limites = resultado["distribuicao"]
    acima = sum(p["motivo"] == "acima do limite superior" for p in resultado["outliers"])
    abaixo = len(resultado["outliers"]) - acima
    insights.append(
        f"Pelo IQR global, {len(resultado['outliers'])} ofertas estão fora dos limites: "
        f"{acima} acima de {moeda(limites['limite_superior'])} e {abaixo} abaixo de "
        f"{moeda(limites['limite_inferior'])}. São extremos da amostra, não erros "
        "comprovados; nenhum registro foi removido."
    )
    return insights


def analisar(dados):
    validar_base(dados)
    precos = dados.preco
    q1, q3 = (float(precos.quantile(q, interpolation="linear")) for q in (0.25, 0.75))
    iqr = q3 - q1
    inferior, superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    extremos = dados.loc[(precos < inferior) | (precos > superior)].copy()
    extremos["motivo"] = extremos.preco.map(
        lambda p: "abaixo do limite inferior" if p < inferior else "acima do limite superior"
    )
    modelos = agrupar(dados, "modelo_gpu", amplitude=True)
    multiplos = sorted(
        (m for m in modelos if m["multiplas_ofertas"]),
        key=lambda m: (-m["amplitude"], m["modelo_gpu"]),
    )
    resultado = {
        "metodologia": {
            "fonte": "data/dados_tratados.csv", "loja": "KaBuM",
            "escopo": "Amostra coletada; não representa todo o mercado nem uma série temporal.",
            "quartis": "Interpolação linear (pandas)",
            "desvio_padrao": "Amostral, ddof=1; null para apenas um registro",
            "outliers": "Preço < Q1 - 1.5*IQR ou preço > Q3 + 1.5*IQR; limites globais",
            "faixas": "(inferior, superior]; cortes escolhidos após inspeção da base",
            "variacao_relevante": "Critério descritivo: n >= 2, amplitude >= R$ 1.000 e >= 20% do mínimo",
            "empates_ranking": "Ordem original da base; exatamente cinco registros quando disponíveis",
            "limitacoes": [
                "Marcas e famílias têm composições e tamanhos diferentes; médias não isolam efeito de marca.",
                "Mesmo modelo de GPU pode incluir memórias e versões diferentes.",
                "Grupos com uma oferta não estimam uma faixa representativa.",
                "Não há medidas de desempenho, histórico de preços ou dados de outras lojas.",
            ],
        },
        "validacao": {
            "colunas": list(dados.columns), "tipo_preco": str(precos.dtype),
            "fabricantes_distintos": int(dados.fabricante.nunique()),
            "modelos_distintos": int(dados.modelo_gpu.nunique()),
            "familias_distintas": int(dados.familia_gpu.nunique()),
        },
        "resumo": {
            "quantidade": len(dados), "preco_medio": float(precos.mean()),
            "mediana": float(precos.median()), "preco_minimo": float(precos.min()),
            "preco_maximo": float(precos.max()),
        },
        "distribuicao": {
            "q1": q1, "q3": q3, "iqr": iqr,
            "desvio_padrao": float(precos.std(ddof=1)) if len(dados) > 1 else None,
            "limite_inferior": inferior, "limite_superior": superior,
        },
        "por_fabricante": agrupar(dados, "fabricante"),
        "por_modelo": modelos,
        "por_familia": agrupar(dados, "familia_gpu"),
        "destaques_modelos": {
            "mais_ofertas": [m for m in modelos if m["quantidade"] == modelos[0]["quantidade"]],
            "maiores_amplitudes": multiplos[:3],
            "variacao_relevante": [m for m in multiplos if m["amplitude"] >= 1000 and m["amplitude_percentual"] >= 20],
        },
        "faixas_preco": distribuir_faixas(precos),
        "mais_baratos": dados.nsmallest(5, "preco", keep="first").to_dict("records"),
        "mais_caros": dados.nlargest(5, "preco", keep="first").to_dict("records"),
        "outliers": extremos.sort_values("preco", ascending=False, kind="stable").to_dict("records"),
    }
    resultado["insights"] = gerar_insights(resultado)
    return resultado


def titulo(texto):
    print("\n" + "=" * 40 + f"\n{texto}\n" + "=" * 40)


def exibir_grupos(grupos, coluna):
    tabela = pd.DataFrame(grupos)
    for campo in ("preco_medio", "mediana", "preco_minimo", "preco_maximo", "amplitude"):
        if campo in tabela:
            tabela[campo] = tabela[campo].map(moeda)
    if "amplitude_percentual" in tabela:
        tabela["amplitude_percentual"] = tabela["amplitude_percentual"].map(lambda x: f"{x:.2f}%")
    print(tabela.to_string(index=False))
    print("Quantidade 1: uma observação; não representa uma faixa de preços.")


def exibir_produtos(produtos):
    if not produtos:
        print("Nenhum registro.")
    for p in produtos:
        print(f"{p['nome_produto']}\n  {p['fabricante']} | {p['modelo_gpu']} | {moeda(p['preco'])}")
        if "motivo" in p:
            print(f"  Motivo: {p['motivo']}")


def exibir_resultados(resultado):
    titulo("ANÁLISE DE PLACAS DE VÍDEO — KABUM")
    print(f"Registros analisados: {resultado['resumo']['quantidade']}")
    print(f"Validação: {resultado['validacao']}")
    for chave, valor in resultado["resumo"].items():
        if chave != "quantidade":
            print(f"{chave}: {moeda(valor)}")
    for chave, valor in resultado["distribuicao"].items():
        print(f"{chave}: {moeda(valor)}")
    print("Desvio-padrão amostral (ddof=1); quartis com interpolação linear.")
    for chave, coluna in (("por_fabricante", "fabricante"), ("por_modelo", "modelo_gpu"), ("por_familia", "familia_gpu")):
        titulo(chave.upper())
        exibir_grupos(resultado[chave], coluna)
    titulo("DESTAQUES POR MODELO")
    print(resultado["metodologia"]["variacao_relevante"])
    for chave, grupos in resultado["destaques_modelos"].items():
        print(f"\n{chave}:")
        for m in grupos:
            print(f"{m['modelo_gpu']}: n={m['quantidade']}, amplitude {moeda(m['amplitude'])} "
                  f"({m['amplitude_percentual']:.2f}% do mínimo)")
    titulo("FAIXAS DE PREÇO")
    for f in resultado["faixas_preco"]:
        print(f"{f['faixa']}: {f['quantidade']} ({f['percentual']:.2f}%)")
    print("Percentuais são arredondados apenas na apresentação; a soma exata é 100%.")
    for chave in ("outliers", "mais_baratos", "mais_caros"):
        titulo(f"{chave.upper()} ({len(resultado[chave])})")
        exibir_produtos(resultado[chave])
    titulo("PRINCIPAIS INSIGHTS")
    for indice, insight in enumerate(resultado["insights"], 1):
        print(f"{indice}. {insight}")
    print("\nLimitações:")
    for limite in resultado["metodologia"]["limitacoes"]:
        print(f"- {limite}")


def main():
    try:
        hash_antes = hashlib.sha256(ARQUIVO_ENTRADA.read_bytes()).hexdigest()
        dados = pd.read_csv(ARQUIVO_ENTRADA, encoding="utf-8-sig")
        resultado = analisar(dados)
        if hashlib.sha256(ARQUIVO_ENTRADA.read_bytes()).hexdigest() != hash_antes:
            raise ValueError("O CSV mudou durante a análise; saída não gravada.")
        resultado["validacao"]["sha256_entrada"] = hash_antes
        conteudo = json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False)
        ARQUIVO_RESULTADOS.write_text(conteudo + "\n", encoding="utf-8")
        exibir_resultados(resultado)
        print(f"\nArquivo salvo em: {ARQUIVO_RESULTADOS}")
        return 0
    except (OSError, ValueError, pd.errors.ParserError) as erro:
        print(f"Não foi possível concluir a análise: {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
