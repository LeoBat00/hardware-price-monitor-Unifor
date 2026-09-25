"""Validação opcional no navegador: python -m unittest test_dashboard -v.

Requer Playwright e Chromium apenas para os testes, não para abrir o dashboard.
"""

import json
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright


RAIZ = Path(__file__).resolve().parent


class DashboardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = json.loads((RAIZ / "data/resultados_analise.json").read_text(encoding="utf-8"))
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 1440, "height": 1000}, offline=True)
        self.page = self.context.new_page()
        self.erros = []
        self.rede = []
        self.page.on("pageerror", lambda erro: self.erros.append(str(erro)))
        self.page.on("console", lambda msg: self.erros.append(msg.text) if msg.type == "error" else None)
        self.page.on("request", lambda req: self.rede.append(req.url) if req.url.startswith(("http:", "https:")) else None)
        self.page.goto((RAIZ / "dashboard/index.html").as_uri())
        self.page.wait_for_function("typeof Chart !== 'undefined' && Object.keys(Chart.instances).length === 3")

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.erros, [])
        self.assertEqual(self.rede, [])

    def dinheiro(self, valor):
        return self.page.evaluate("valor => new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(valor)", valor)

    def test_dados_e_cards_correspondem_ao_json(self):
        self.assertEqual(self.page.evaluate("dadosAnalise"), self.dados)
        for id_html, campo in [("quantidade", "quantidade"), ("preco-medio", "preco_medio"), ("preco-minimo", "preco_minimo"), ("preco-maximo", "preco_maximo")]:
            valor = self.dados["resumo"][campo]
            esperado = str(valor) if campo == "quantidade" else self.dinheiro(valor)
            self.assertEqual(self.page.locator(f"#{id_html}").inner_text(), esperado)
        self.assertEqual(self.dados["resumo"]["quantidade"], 86)
        self.assertTrue(self.page.locator("#erro").is_hidden())

    def test_graficos_usam_todos_os_grupos_e_valores(self):
        for id_html, linhas, campo in [
            ("grafico-faixas", self.dados["faixas_preco"], "quantidade"),
            ("grafico-modelos", sorted(self.dados["por_modelo"], key=lambda item: -item["quantidade"]), "quantidade"),
            ("grafico-medias", sorted(self.dados["por_modelo"], key=lambda item: -item["preco_medio"]), "preco_medio"),
        ]:
            grafico = self.page.evaluate("id => { const c = Chart.getChart(id); return {labels: c.data.labels, values: c.data.datasets[0].data, width: c.width, height: c.height}; }", id_html)
            self.assertEqual(grafico["values"], [item[campo] for item in linhas])
            self.assertGreater(grafico["width"], 0)
            self.assertGreater(grafico["height"], 0)
            if id_html != "grafico-faixas":
                self.assertEqual(grafico["labels"], [item["modelo_gpu"] for item in linhas])
            else:
                self.assertEqual(len(grafico["labels"]), len(linhas))

    def test_insights_interpretacoes_e_limitacoes(self):
        self.assertEqual(self.page.locator("#lista-insights li").all_text_contents(), self.dados["insights"])
        self.assertEqual(self.page.locator("#limitacoes li").all_text_contents(), self.dados["metodologia"]["limitacoes"])
        for id_html in ["faixas", "modelos", "medias"]:
            esperado = self.page.evaluate("id => textosGraficos[id]", id_html)
            self.assertEqual(self.page.locator(f"#texto-{id_html}").inner_text(), esperado)
            self.assertIn("amostra", esperado)

    def test_outliers_e_ranking_preservam_todos_os_campos(self):
        for id_html, campo in [("tabela-outliers", "outliers"), ("tabela-baratos", "mais_baratos")]:
            linhas = self.page.locator(f"#{id_html} tbody tr")
            self.assertEqual(linhas.count(), len(self.dados[campo]))
            for i, item in enumerate(self.dados[campo]):
                self.assertEqual(linhas.nth(i).locator("td").all_text_contents(), [
                    item["nome_produto"], item["fabricante"], item["modelo_gpu"], self.dinheiro(item["preco"]),
                ])

    def test_tabelas_alternativas_e_navegacao_por_teclado(self):
        for id_html, quantidade in [("faixas", len(self.dados["faixas_preco"])), ("modelos", len(self.dados["por_modelo"])), ("medias", len(self.dados["por_modelo"]))]:
            painel = self.page.locator(f"#tabela-{id_html}")
            detalhes = painel.locator("..")
            detalhes.locator("summary").focus()
            self.page.keyboard.press("Enter")
            self.assertTrue(painel.is_visible())
            self.assertEqual(painel.locator("tbody tr").count(), quantidade)
            self.assertGreater(painel.locator("th[scope=col]").count(), 0)
        self.assertEqual(self.page.locator("canvas[role=img][aria-labelledby][aria-describedby]").count(), 3)

    def test_layout_em_telas_menores(self):
        for largura in [768, 390, 320]:
            with self.subTest(largura=largura):
                self.page.set_viewport_size({"width": largura, "height": 844})
                self.page.wait_for_timeout(200)
                medidas = self.page.evaluate("({client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth})")
                self.assertLessEqual(medidas["scroll"], medidas["client"])
                for canvas in self.page.locator("canvas").all():
                    caixa = canvas.bounding_box()
                    self.assertGreater(caixa["width"], 0)
                    self.assertLessEqual(caixa["x"] + caixa["width"], largura)
                rotacao = self.page.evaluate("Chart.getChart('grafico-faixas').scales.x.labelRotation")
                self.assertEqual(rotacao, 55)


if __name__ == "__main__":
    unittest.main()
