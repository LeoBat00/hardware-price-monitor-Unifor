"""Testes pequenos com bases sintéticas; não coletam nem alteram os CSVs reais."""

import json
import statistics
import unittest

import pandas as pd

import analise as a


def base(precos):
    return pd.DataFrame([
        dict(nome_produto=f"Placa {i}", preco=p, loja="KaBuM", url=f"https://exemplo.test/{i}",
             categoria="Placa de vídeo", fabricante="ASUS", modelo_gpu="RTX 5060", familia_gpu="RTX 50")
        for i, p in enumerate(precos)
    ], columns=a.COLUNAS)


class AnaliseTests(unittest.TestCase):
    def test_estatisticas_iqr_e_preservacao(self):
        dados = base([1, 2, 3, 4, 100])
        copia = dados.copy(deep=True)
        r = a.analisar(dados)
        self.assertEqual(r["resumo"]["preco_medio"], 22)
        self.assertEqual(r["resumo"]["mediana"], 3)
        self.assertEqual(r["distribuicao"]["q1"], 2)
        self.assertEqual(r["distribuicao"]["q3"], 4)
        self.assertEqual(r["distribuicao"]["iqr"], 2)
        self.assertAlmostEqual(r["distribuicao"]["desvio_padrao"], statistics.stdev([1, 2, 3, 4, 100]))
        self.assertEqual([p["preco"] for p in r["outliers"]], [100])
        self.assertEqual(r["outliers"][0]["motivo"], "acima do limite superior")
        pd.testing.assert_frame_equal(dados, copia)

    def test_faixas_fronteiras_sem_sobreposicao(self):
        r = a.analisar(base([1500, 1500.01, 3000, 3000.01, 5000, 5000.01, 8000, 8000.01, 12000, 12000.01]))
        self.assertEqual([f["quantidade"] for f in r["faixas_preco"]], [1, 2, 2, 2, 2, 1])
        self.assertAlmostEqual(sum(f["percentual"] for f in r["faixas_preco"]), 100)

    def test_grupos_isolados_e_amplitude(self):
        dados = base([2000, 3500, 5000])
        dados.loc[2, ["modelo_gpu", "fabricante"]] = ["RTX 5070", "MSI"]
        r = a.analisar(dados)
        grupos = {g["modelo_gpu"]: g for g in r["por_modelo"]}
        self.assertEqual(grupos["RTX 5060"]["amplitude"], 1500)
        self.assertEqual(grupos["RTX 5060"]["mediana"], 2750)
        self.assertFalse(grupos["RTX 5070"]["multiplas_ofertas"])
        self.assertEqual(len(r["destaques_modelos"]["variacao_relevante"]), 1)
        self.assertEqual(sum(g["quantidade"] for g in r["por_fabricante"]), 3)

    def test_base_unitaria_json_valido_e_iqr_zero(self):
        r = a.analisar(base([2000]))
        self.assertIsNone(r["distribuicao"]["desvio_padrao"])
        self.assertEqual(r["outliers"], [])
        self.assertEqual(r["destaques_modelos"]["maiores_amplitudes"], [])
        json.dumps(r, allow_nan=False)
        self.assertEqual(a.analisar(base([2000] * 5))["outliers"], [])

    def test_outlier_inferior_e_limite_exato(self):
        r = a.analisar(base([1, 100, 101, 102, 103]))
        self.assertEqual(r["outliers"][0]["motivo"], "abaixo do limite inferior")
        # Q1=2, Q3=4, limite superior=7: igualdade não é outlier.
        self.assertEqual(a.analisar(base([1, 2, 3, 4, 7]))["outliers"], [])

    def test_rejeita_base_invalida(self):
        for precos in ([], [0], [-1], [float("inf")], [float("nan")], ["R$ 10"], [True]):
            with self.subTest(precos=precos), self.assertRaises(ValueError):
                a.analisar(base(precos))
        dados = base([1, 2]); dados.loc[1, "url"] = dados.loc[0, "url"]
        with self.assertRaises(ValueError):
            a.analisar(dados)
        with self.assertRaises(ValueError):
            a.analisar(base([1]).drop(columns="fabricante"))

    def test_moeda_e_ranking_com_empates(self):
        self.assertEqual(a.moeda(2799.9), "R$ 2.799,90")
        dados = base([1000] * 6)
        r = a.analisar(dados)
        self.assertEqual([p["url"] for p in r["mais_caros"]], dados.url.iloc[:5].tolist())


if __name__ == "__main__":
    unittest.main()
