"""Copia os resultados existentes para um script local; não refaz a análise."""

import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
ORIGEM = RAIZ / "data" / "resultados_analise.json"
DESTINO = RAIZ / "dashboard" / "dados.js"


def moeda(valor):
    return f"R$ {valor:,.2f}".translate(str.maketrans({",": ".", ".": ","}))


def preparar():
    dados = json.loads(ORIGEM.read_text(encoding="utf-8"))
    # Ordena estatísticas já prontas apenas para descrever o que será mostrado.
    quantidade = sorted(dados["por_modelo"], key=lambda item: -item["quantidade"])
    medias = sorted(dados["por_modelo"], key=lambda item: -item["preco_medio"])
    destaques_quantidade = "; ".join(
        f"{item['modelo_gpu']} ({item['quantidade']} ofertas)" for item in quantidade[:3]
    )
    destaques_medias = "; ".join(
        f"{item['modelo_gpu']} ({moeda(item['preco_medio'])})" for item in medias[:2]
    )
    textos = {
        "faixas": dados["insights"][0],
        "modelos": f"Na amostra analisada, os primeiros modelos por quantidade são: {destaques_quantidade}.",
        "medias": (
            f"As maiores médias entre os modelos da amostra são: {destaques_medias}. "
            "Um mesmo modelo pode reunir diferentes versões e capacidades de memória."
        ),
    }
    # Arquivo externo (não HTML inline), carregável também pelo protocolo file://.
    conteudo = "// Gerado por preparar_dashboard.py. Não editar manualmente.\n"
    conteudo += "const dadosAnalise = " + json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False) + ";\n"
    conteudo += "const textosGraficos = " + json.dumps(textos, ensure_ascii=False, indent=2, allow_nan=False) + ";\n"
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(conteudo, encoding="utf-8")
    print(f"Dashboard atualizado: {DESTINO}")


if __name__ == "__main__":
    preparar()
