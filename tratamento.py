"""Pré-processa o CSV existente, sem executar coleta nem alterar os dados brutos."""

import hashlib
import math
import re
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd


PASTA_DADOS = Path(__file__).resolve().parent / "data"
ARQUIVO_BRUTO = PASTA_DADOS / "dados_brutos.csv"
ARQUIVO_TRATADO = PASTA_DADOS / "dados_tratados.csv"
COLUNAS = ["nome_produto", "preco", "loja", "url", "categoria"]
NAO_IDENTIFICADO = "Não identificado"
INVISIVEIS = re.compile("[\u200b\u2060\ufeff\u00ad]")

# Marcas efetivamente observadas nas placas da base; NVIDIA/AMD/Intel são GPUs,
# não substituem a marca da placa. Mais de uma marca reconhecida gera incerteza.
FABRICANTES = (
    "ASRock", "ASUS", "Galax", "Gigabyte", "Husky", "Inno3D",
    "MSI", "Palit", "PCYes", "PNY", "PowerColor", "XFX",
)
PADRAO_NVIDIA = re.compile(r"\b(RTX|GTX)\s*(\d{4})(?:\s*(Ti|SUPER))?\b", re.I)
PADRAO_AMD = re.compile(r"\b(RX)\s*(\d{3,4})(?:\s*(XT))?\b", re.I)
PADRAO_INTEL = re.compile(r"\bArc\s*(B\d{3})\b", re.I)
# A inspeção encontrou dois suportes e um cabo riser rotulados como placas.
# A regra usa o tipo no início do nome, sem listar produtos ou suas URLs.
PADRAO_ACESSORIO = re.compile(r"^(?:suporte\b|cabo\b)", re.I)


def limpar_texto(valor):
    if pd.isna(valor):
        return ""
    return re.sub(r"\s+", " ", INVISIVEIS.sub("", str(valor))).strip()


def converter_preco(valor):
    """Aceita decimal com ponto ou formato brasileiro; rejeita ambiguidades."""
    if pd.isna(valor) or isinstance(valor, bool):
        return None
    texto = str(valor).strip()
    tem_moeda = texto.startswith("R$")
    if tem_moeda:
        texto = texto[2:].strip()

    if re.fullmatch(r"\d+(?:\.\d{1,2})?", texto):
        numero = texto
    elif re.fullmatch(r"(?:\d+|\d{1,3}(?:\.\d{3})+),\d{1,2}", texto):
        numero = texto.replace(".", "").replace(",", ".")
    elif tem_moeda and re.fullmatch(r"\d{1,3}(?:\.\d{3})+", texto):
        numero = texto.replace(".", "")
    else:
        # Ex.: 2.799 sem moeda é ambíguo; não presumir milhar nem arredondar.
        return None
    preco = float(numero)
    return preco if math.isfinite(preco) and preco > 0 else None


def url_valida(valor):
    if not valor.startswith(("http://", "https://")) or re.search(r"\s", valor):
        return False
    try:
        return bool(urlsplit(valor).hostname)
    except ValueError:
        return False


def identificar_fabricante(nome):
    marcas = [marca for marca in FABRICANTES if re.search(rf"\b{re.escape(marca)}\b", nome, re.I)]
    return marcas[0] if len(marcas) == 1 else NAO_IDENTIFICADO


def identificar_modelo(nome):
    modelos = set()
    for padrao in (PADRAO_NVIDIA, PADRAO_AMD):
        for linha, numero, sufixo in padrao.findall(nome):
            modelo = f"{linha.upper()} {numero}"
            if sufixo:
                modelo += " " + ("Ti" if sufixo.upper() == "TI" else sufixo.upper())
            modelos.add(modelo)
    modelos.update(f"Arc {codigo.upper()}" for codigo in PADRAO_INTEL.findall(nome))
    # Repetições do mesmo modelo no título/SKU são aceitas; conflitos não.
    return next(iter(modelos)) if len(modelos) == 1 else NAO_IDENTIFICADO


def identificar_familia(modelo):
    nvidia = re.fullmatch(r"(RTX|GTX) (\d{4})(?: (?:Ti|SUPER))?", modelo)
    if nvidia:
        return f"{nvidia[1]} {nvidia[2][:2]}"
    amd = re.fullmatch(r"RX (\d{3,4})(?: XT)?", modelo)
    if amd:
        return "RX " + amd[1][0] + "0" * (len(amd[1]) - 1)
    if re.fullmatch(r"Arc B\d{3}", modelo):
        return "Arc B"
    return NAO_IDENTIFICADO


def diagnosticar(dados):
    """Contagens de qualidade antes de qualquer remoção ou transformação."""
    ausentes = {}
    espacos = {}
    for coluna in COLUNAS:
        textos = dados[coluna].fillna("").astype(str)
        ausentes[coluna] = int(textos.map(limpar_texto).eq("").sum())
        espacos[coluna] = {
            "bordas": int(textos.ne(textos.str.strip()).sum()),
            "repetidos_ou_quebras": int(textos.str.contains(r"\s{2,}|[\r\n\t]").sum()),
            "invisiveis": int(textos.str.contains(INVISIVEIS).sum()),
        }
    precos = dados["preco"].fillna("").astype(str)
    return {
        "linhas": len(dados), "colunas": len(dados.columns),
        "ausentes": ausentes, "espacos": espacos,
        "duplicados_completos": int(dados.duplicated().sum()),
        "urls_duplicadas": int(dados.loc[dados.url.map(limpar_texto).ne(""), "url"].duplicated().sum()),
        "precos_com_moeda": int(precos.str.contains("R$", regex=False).sum()),
        "precos_com_virgula": int(precos.str.contains(",", regex=False).sum()),
        "precos_com_milhar_br": int(precos.str.contains(r"\d\.\d{3}(?:,|\.|$)").sum()),
        "exemplos_precos": precos.head(5).tolist(),
        "exemplos_nomes": dados.nome_produto.head(3).tolist(),
        "lojas": dados.loja.unique().tolist(),
        "categorias": dados.categoria.unique().tolist(),
    }


def tratar_dados(brutos):
    faltantes = set(COLUNAS) - set(brutos.columns)
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(faltantes))}")
    dados = brutos[COLUNAS].copy()
    resumo = {"inicial": len(dados), "removidos": {}}
    for coluna in ("nome_produto", "loja", "categoria"):
        dados[coluna] = dados[coluna].map(limpar_texto)
    # URLs só perdem espaços externos; parâmetros e caminhos são preservados.
    dados["url"] = dados["url"].fillna("").astype(str).str.strip()
    resumo["nomes_limpos"] = int(dados.nome_produto.ne(brutos.nome_produto).sum())
    precos = dados.preco.map(converter_preco)
    preco_ausente = dados.preco.map(limpar_texto).eq("")
    resumo["precos_convertidos"] = int(precos.notna().sum())
    resumo["precos_invalidos"] = int((precos.isna() & ~preco_ausente).sum())

    # Remoções sequenciais: cada linha recebe somente o primeiro motivo aplicável.
    ausente = dados.apply(lambda c: c.map(limpar_texto).eq("")).any(axis=1)
    resumo["removidos"]["essenciais_ausentes"] = int(ausente.sum())
    dados = dados.loc[~ausente].copy()
    dados["preco"] = precos.loc[dados.index].astype(float)

    filtros = (
        ("precos_invalidos", lambda d: d.preco.isna()),
        ("urls_invalidas", lambda d: ~d.url.map(url_valida).astype(bool)),
        ("acessorios_fora_escopo", lambda d: d.nome_produto.str.match(PADRAO_ACESSORIO)),
        ("duplicados_completos", lambda d: d.duplicated()),
        ("urls_duplicadas", lambda d: d.duplicated(subset="url")),
    )
    for motivo, selecionar in filtros:
        rejeitados = selecionar(dados).astype(bool)
        resumo["removidos"][motivo] = int(rejeitados.sum())
        dados = dados.loc[~rejeitados].copy()

    dados["fabricante"] = dados.nome_produto.map(identificar_fabricante)
    dados["modelo_gpu"] = dados.nome_produto.map(identificar_modelo)
    dados["familia_gpu"] = dados.modelo_gpu.map(identificar_familia)
    resumo["atributos"] = {}
    for coluna in ("fabricante", "modelo_gpu", "familia_gpu"):
        identificados = dados[coluna].ne(NAO_IDENTIFICADO)
        resumo["atributos"][coluna] = {
            "identificados": int(identificados.sum()),
            "nao_identificados": int((~identificados).sum()),
            "valores_distintos": sorted(dados.loc[identificados, coluna].unique().tolist()),
        }
    resumo["final"] = len(dados)
    return dados.reset_index(drop=True), resumo


def exibir_diagnostico(diagnostico, tipos):
    print(f"Registros brutos: {diagnostico['linhas']}; colunas: {diagnostico['colunas']}")
    print(f"Tipos inferidos pelo pandas: {tipos}")
    print("Processamento lê todas as colunas como texto para não perder formatos.")
    print("\nValores ausentes:")
    for coluna, total in diagnostico["ausentes"].items():
        print(f"{coluna}: {total}")
    print(f"Duplicados completos: {diagnostico['duplicados_completos']}")
    print(f"URLs duplicadas: {diagnostico['urls_duplicadas']}")
    print(f"Preços com R$: {diagnostico['precos_com_moeda']}")
    print(f"Preços com vírgula: {diagnostico['precos_com_virgula']}")
    print(f"Preços com possível separador de milhar brasileiro: {diagnostico['precos_com_milhar_br']}")
    print(f"Exemplos de preços: {diagnostico['exemplos_precos']}")
    print(f"Exemplos de nomes: {diagnostico['exemplos_nomes']}")
    print(f"Lojas: {diagnostico['lojas']}; categorias: {diagnostico['categorias']}")
    print("\nEspaços e caracteres por coluna:")
    for coluna, contagens in diagnostico["espacos"].items():
        print(f"{coluna}: {contagens}")


def main():
    print("=" * 40 + "\nPRÉ-PROCESSAMENTO DOS DADOS\n" + "=" * 40)
    try:
        hash_antes = hashlib.sha256(ARQUIVO_BRUTO.read_bytes()).hexdigest()
        brutos = pd.read_csv(ARQUIVO_BRUTO, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        if set(COLUNAS) - set(brutos.columns):
            raise ValueError("O CSV bruto não contém as cinco colunas obrigatórias.")
        tipos = pd.read_csv(ARQUIVO_BRUTO, encoding="utf-8-sig").dtypes.astype(str).to_dict()
        exibir_diagnostico(diagnosticar(brutos), tipos)
        tratados, resumo = tratar_dados(brutos)
        print(f"\nPreços convertidos na entrada: {resumo['precos_convertidos']}")
        print(f"Preços inválidos (não vazios): {resumo['precos_invalidos']}")
        print(f"Nomes com limpeza de espaços/invisíveis: {resumo['nomes_limpos']}")
        for motivo, total in resumo["removidos"].items():
            print(f"Removidos — {motivo}: {total}")
        print(f"Total removido: {resumo['inicial'] - resumo['final']}")
        print("\nATRIBUTOS DERIVADOS")
        for coluna, contagem in resumo["atributos"].items():
            print(f"{coluna}: {contagem['identificados']} identificados; "
                  f"{contagem['nao_identificados']} não identificados; "
                  f"{len(contagem['valores_distintos'])} valores distintos")
        if hashlib.sha256(ARQUIVO_BRUTO.read_bytes()).hexdigest() != hash_antes:
            raise ValueError("O arquivo bruto mudou durante a execução. Saída não gravada.")
        if tratados.empty:
            raise ValueError("Nenhum registro utilizável. Arquivo tratado anterior preservado.")
        tratados.to_csv(ARQUIVO_TRATADO, index=False, encoding="utf-8-sig")
        print(f"\nRegistros tratados: {len(tratados)}")
        print(f"Arquivo salvo em: {ARQUIVO_TRATADO}")
        print(f"SHA-256 do bruto preservado: {hash_antes}")
        return 0
    except (OSError, ValueError, pd.errors.ParserError) as erro:
        print(f"Não foi possível concluir o tratamento: {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
