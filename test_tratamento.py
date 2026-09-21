"""Verificações locais do tratamento; não consultam a web nem usam o CSV real."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

import tratamento as t


class TratamentoTests(unittest.TestCase):
    def registro(self, **alteracoes):
        registro = dict(
            nome_produto="Placa de Vídeo ASUS RTX 5060 Ti",
            preco="2799.99", loja="KaBuM", url="https://exemplo.test/produto/1?a=2&b=3",
            categoria="Placa de vídeo",
        )
        return dict(registro, **alteracoes)

    def test_precos_formatos_aceitos(self):
        for entrada, esperado in (
            ("2799.99", 2799.99), ("R$ 2.799,90", 2799.90),
            ("R$ 899,99", 899.99), ("R$\u00a02.799,90", 2799.90),
            ("12199.9", 12199.9), ("12000", 12000.0),
            ("R$ 2.799", 2799.0), ("1.234.567,89", 1234567.89),
            (2799.99, 2799.99), (" 899,99 ", 899.99),
        ):
            with self.subTest(entrada=entrada):
                self.assertEqual(t.converter_preco(entrada), esperado)

    def test_precos_invalidos_ambiguos_ou_parcelas(self):
        for entrada in (None, pd.NA, float("nan"), "", "NaN", "inf", "-10", "0",
                        "2.799", "2,799", "2,799.90", "2.79,90", "27 99", "R$ R$ 10",
                        "12x de R$ 200,00", "a partir de R$ 899,99", True):
            with self.subTest(entrada=entrada):
                self.assertIsNone(t.converter_preco(entrada))

    def test_limpeza_conservadora(self):
        nome = " \u200bPlaca  de Vídeo\nASUS\tRTX 5060 Ti - SKU-123\ufeff "
        self.assertEqual(t.limpar_texto(nome), "Placa de Vídeo ASUS RTX 5060 Ti - SKU-123")
        brutos = pd.DataFrame([self.registro(nome_produto=nome, url="  https://exemplo.test/p?a=1&b=2  ")])
        copia = brutos.copy(deep=True)
        tratados, _ = t.tratar_dados(brutos)
        pd.testing.assert_frame_equal(brutos, copia)
        self.assertEqual(tratados.iloc[0].url, "https://exemplo.test/p?a=1&b=2")

    def test_modelos_e_familias(self):
        for nome, modelo, familia in (
            ("Palit RTX5060Ti INFINITY", "RTX 5060 Ti", "RTX 50"),
            ("ASUS RTX 4070 Ti", "RTX 4070 Ti", "RTX 40"),
            ("Husky RTX 3060 TI", "RTX 3060 Ti", "RTX 30"),
            ("PowerColor RX 9070 XT - RX9070XT 16G-A", "RX 9070 XT", "RX 9000"),
            ("ASRock RX 7600", "RX 7600", "RX 7000"),
            ("Husky RX 580", "RX 580", "RX 500"),
            ("PCYes GTX 1660 SUPER", "GTX 1660 SUPER", "GTX 16"),
            ("ASRock Intel Arc B580", "Arc B580", "Arc B"),
        ):
            with self.subTest(nome=nome):
                self.assertEqual(t.identificar_modelo(nome), modelo)
                self.assertEqual(t.identificar_familia(modelo), familia)

    def test_desconhecidos_e_conflitos_nao_sao_forcados(self):
        self.assertEqual(t.identificar_fabricante("GPU AMD Radeon RX 7600"), t.NAO_IDENTIFICADO)
        self.assertEqual(t.identificar_fabricante("ASUS ou MSI RTX 5060"), t.NAO_IDENTIFICADO)
        self.assertEqual(t.identificar_modelo("GPU RTX 5060 ou RTX 5070"), t.NAO_IDENTIFICADO)
        self.assertEqual(t.identificar_modelo("Placa sem modelo"), t.NAO_IDENTIFICADO)
        self.assertEqual(t.identificar_familia(t.NAO_IDENTIFICADO), t.NAO_IDENTIFICADO)
        tratados, _ = t.tratar_dados(pd.DataFrame([self.registro(nome_produto="Placa sem modelo")]))
        self.assertEqual(len(tratados), 1)
        self.assertEqual(tratados.iloc[0].fabricante, t.NAO_IDENTIFICADO)

    def test_remocoes_e_duplicidade_por_url_apos_validacao(self):
        linhas = [
            self.registro(preco="inválido"), self.registro(), self.registro(),
            self.registro(preco="3000"),
            self.registro(url="https://exemplo.test/outro"),
            self.registro(nome_produto=""),
            self.registro(url="javascript:alert(1)"),
            self.registro(nome_produto="Suporte para GPU Rise Mode"),
            self.registro(nome_produto="Cabo Extensor PCI Express Rise Mode Riser"),
        ]
        tratados, resumo = t.tratar_dados(pd.DataFrame(linhas))
        self.assertEqual(len(tratados), 2)  # Mesmo nome, URLs distintas: preservar.
        self.assertEqual(tratados.iloc[0].preco, 2799.99)
        self.assertEqual(resumo["removidos"], dict(
            essenciais_ausentes=1, precos_invalidos=1, urls_invalidas=1,
            acessorios_fora_escopo=2, duplicados_completos=1, urls_duplicadas=1,
        ))
        self.assertEqual(sum(resumo["removidos"].values()) + len(tratados), len(linhas))

    def test_urls(self):
        for url in ("", "https://", "ftp://exemplo.test", "https://exemplo.test/a b", "http://["):
            self.assertFalse(t.url_valida(url))
        self.assertTrue(t.url_valida("https://exemplo.test/p?a=2&b=3"))

    def test_base_sem_registros_utilizaveis(self):
        for linhas in ([], [self.registro(nome_produto="")], [self.registro(preco="inválido")]):
            with self.subTest(linhas=linhas):
                tratados, _ = t.tratar_dados(pd.DataFrame(linhas, columns=t.COLUNAS))
                self.assertTrue(tratados.empty)

    def test_colunas_ausentes(self):
        with self.assertRaises(ValueError):
            t.tratar_dados(pd.DataFrame({"preco": [1]}))

    def test_execucao_grava_apenas_tratado(self):
        with tempfile.TemporaryDirectory() as pasta:
            bruto = Path(pasta) / "dados_brutos.csv"
            tratado = Path(pasta) / "dados_tratados.csv"
            pd.DataFrame([self.registro(preco="R$ 2.799,90")]).to_csv(bruto, index=False)
            antes = bruto.read_bytes()
            with patch.object(t, "ARQUIVO_BRUTO", bruto), patch.object(t, "ARQUIVO_TRATADO", tratado), patch("builtins.print"):
                self.assertEqual(t.main(), 0)
            self.assertEqual(bruto.read_bytes(), antes)
            saida = pd.read_csv(tratado)
            self.assertEqual(saida.iloc[0].preco, 2799.90)
            self.assertEqual(len(saida.columns), 8)


if __name__ == "__main__":
    unittest.main()
