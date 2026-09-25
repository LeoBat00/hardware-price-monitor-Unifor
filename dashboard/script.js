"use strict";

(() => {
  const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
  const inteiro = new Intl.NumberFormat("pt-BR");
  const percentual = new Intl.NumberFormat("pt-BR", { style: "percent", maximumFractionDigits: 2 });
  const texto = (id, valor) => { document.getElementById(id).textContent = valor; };

  function tabela(id, legenda, colunas, linhas) {
    const table = document.createElement("table");
    const caption = table.createCaption();
    caption.textContent = legenda;
    const header = table.createTHead().insertRow();
    colunas.forEach(({ titulo, classe }) => {
      const th = document.createElement("th");
      th.scope = "col";
      th.textContent = titulo;
      if (classe) th.className = classe;
      header.append(th);
    });
    const body = table.createTBody();
    linhas.forEach(item => {
      const row = body.insertRow();
      colunas.forEach(({ campo, formato, classe }) => {
        const cell = row.insertCell();
        cell.textContent = formato ? formato(item[campo]) : item[campo];
        if (classe) cell.className = classe;
      });
    });
    document.getElementById(id).replaceChildren(table);
  }

  function lista(id, itens) {
    const fragment = document.createDocumentFragment();
    itens.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      fragment.append(li);
    });
    document.getElementById(id).replaceChildren(fragment);
  }

  function grafico(id, rotulos, valores, { horizontal = false, monetario = false, cor = "#087e80", tooltipLabels = rotulos } = {}) {
    const valueAxis = {
      beginAtZero: true,
      border: { display: false },
      grid: { color: "#e6edef" },
      ticks: {
        precision: monetario ? undefined : 0,
        maxTicksLimit: monetario ? 5 : 7,
        callback: value => monetario ? brl.format(value) : inteiro.format(value),
      },
      title: { display: true, text: monetario ? "Preço médio (R$)" : "Quantidade de ofertas", color: "#52666e", font: { size: 10 } },
    };
    const categoryAxis = { grid: { display: false }, border: { display: false }, ticks: { autoSkip: false, maxRotation: 0, font: { size: 10 } } };
    return new Chart(document.getElementById(id), {
      type: "bar",
      data: { labels: rotulos, datasets: [{ label: monetario ? "Preço médio" : "Ofertas", data: valores, backgroundColor: cor, borderRadius: 3, maxBarThickness: horizontal ? 16 : 44 }] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        indexAxis: horizontal ? "y" : "x",
        onResize: (chart, size) => {
          if (!horizontal) {
            const rotacao = size.width < 500 ? 55 : 0;
            chart.options.scales.x.ticks.minRotation = rotacao;
            chart.options.scales.x.ticks.maxRotation = rotacao;
          }
        },
        layout: { padding: { top: 4, right: 8 } },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#172f37",
            padding: 12,
            callbacks: {
              title: items => tooltipLabels[items[0].dataIndex],
              label: context => monetario ? brl.format(context.raw) : `${inteiro.format(context.raw)} ofertas`,
            },
          },
        },
        scales: horizontal ? { x: valueAxis, y: categoryAxis } : { x: categoryAxis, y: valueAxis },
      },
    });
  }

  try {
    if (typeof dadosAnalise === "undefined" || typeof textosGraficos === "undefined") {
      throw new Error("Não foi possível carregar os dados. Mantenha dados.js na mesma pasta do dashboard e gere-o com preparar_dashboard.py.");
    }
    const dados = dadosAnalise;
    texto("quantidade", inteiro.format(dados.resumo.quantidade));
    texto("preco-medio", brl.format(dados.resumo.preco_medio));
    texto("preco-minimo", brl.format(dados.resumo.preco_minimo));
    texto("preco-maximo", brl.format(dados.resumo.preco_maximo));
    ["faixas", "modelos", "medias"].forEach(id => texto(`texto-${id}`, textosGraficos[id]));
    lista("lista-insights", dados.insights);
    lista("limitacoes", dados.metodologia.limitacoes);
    texto("total-outliers", `${inteiro.format(dados.outliers.length)} ofertas identificadas`);

    const colunasProdutos = [
      { titulo: "Produto", campo: "nome_produto", classe: "product-name" },
      { titulo: "Fabricante", campo: "fabricante" },
      { titulo: "Modelo", campo: "modelo_gpu" },
      { titulo: "Preço", campo: "preco", formato: brl.format, classe: "numeric" },
    ];
    tabela("tabela-outliers", "Todos os outliers identificados na análise, sem remoção de registros.", colunasProdutos, dados.outliers);
    tabela("tabela-baratos", "Ordem crescente de preço; empates preservam a ordem da análise.", colunasProdutos, dados.mais_baratos);

    // Apenas ordenação e apresentação de estatísticas prontas. Não calcula médias,
    // faixas, rankings de produtos ou novos insights a partir das ofertas.
    const modelos = [...dados.por_modelo].sort((a, b) => b.quantidade - a.quantidade);
    const medias = [...dados.por_modelo].sort((a, b) => b.preco_medio - a.preco_medio);
    tabela("tabela-faixas", "Distribuição por faixa de preço", [
      { titulo: "Faixa de preço", campo: "faixa" },
      { titulo: "Ofertas", campo: "quantidade", formato: inteiro.format, classe: "numeric" },
      { titulo: "Percentual", campo: "percentual", formato: valor => percentual.format(valor / 100), classe: "numeric" },
    ], dados.faixas_preco);
    tabela("tabela-modelos", "Quantidade por modelo de GPU", [
      { titulo: "Modelo", campo: "modelo_gpu" },
      { titulo: "Ofertas", campo: "quantidade", formato: inteiro.format, classe: "numeric" },
    ], modelos);
    tabela("tabela-medias", "Preço médio por modelo de GPU", [
      { titulo: "Modelo", campo: "modelo_gpu" },
      { titulo: "Ofertas", campo: "quantidade", formato: inteiro.format, classe: "numeric" },
      { titulo: "Preço médio", campo: "preco_medio", formato: brl.format, classe: "numeric" },
    ], medias);

    if (typeof Chart === "undefined") {
      throw new Error("Não foi possível carregar os gráficos. Confira o arquivo vendor/chart.umd.js. Os valores continuam disponíveis nas tabelas.");
    }
    Chart.defaults.font.family = 'system-ui, -apple-system, "Segoe UI", sans-serif';
    Chart.defaults.color = "#52666e";
    Chart.defaults.font.size = 11;
    // Quebras de linha mantêm os intervalos legíveis em telas pequenas.
    const rotulosFaixas = dados.faixas_preco.map(faixa => {
      const inferior = faixa.limite_inferior_exclusivo;
      const superior = faixa.limite_superior_inclusivo;
      if (inferior === 0) return ["Até", brl.format(superior)];
      if (superior === null) return ["Acima de", brl.format(inferior)];
      return ["> " + brl.format(inferior), "até", brl.format(superior)];
    });
    grafico("grafico-faixas", rotulosFaixas, dados.faixas_preco.map(item => item.quantidade), { tooltipLabels: dados.faixas_preco.map(item => item.faixa) });
    grafico("grafico-modelos", modelos.map(item => item.modelo_gpu), modelos.map(item => item.quantidade), { horizontal: true });
    grafico("grafico-medias", medias.map(item => item.modelo_gpu), medias.map(item => item.preco_medio), { horizontal: true, monetario: true, cor: "#315d79" });
  } catch (erro) {
    texto("erro", erro.message);
    document.getElementById("erro").hidden = false;
    console.error(erro);
  }
})();
