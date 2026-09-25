# Monitoramento de preços — etapa 6

## Dashboard local

Abra **`dashboard/index.html`** diretamente no navegador. A página funciona
sem internet, servidor ou instalação de dependências: HTML, CSS, JavaScript,
Chart.js e os dados já estão incluídos na pasta `dashboard/`.

O dashboard apresenta quatro indicadores (quantidade, média, mínimo e máximo),
três gráficos com interpretações, os quatro insights da análise, todos os sete
outliers e o ranking dos cinco menores preços. Os gráficos mostram:

- Distribuição por faixa de preço: `faixas_preco`, com quantidade de ofertas.
- Quantidade por modelo: `por_modelo`, com todos os 17 modelos.
- Preço médio por modelo: `por_modelo.preco_medio`, em reais e em eixo separado.

Os valores vêm de `data/resultados_analise.json`, convertido integralmente para
`dashboard/dados.js`. O frontend apenas ordena e formata os resultados prontos;
não recalcula a análise. As interpretações dos gráficos são preparadas no mesmo
conversor a partir dos resultados existentes. Os insights são exibidos sem
alterações de redação.

Se o JSON for atualizado em outra etapa, regenere sua cópia estática:

```sh
python preparar_dashboard.py
```

O conversor usa somente a biblioteca padrão do Python, independe do diretório
de execução e não altera o JSON, os CSVs ou os scripts das etapas anteriores.
Não é necessário executar novamente coleta, tratamento ou análise para abrir
o dashboard atual.

O layout usa fundo claro, paleta consistente e se adapta a telas menores.
Os gráficos têm títulos, descrições e tabelas alternativas acessíveis pelo
teclado. As tabelas de produtos permitem rolagem horizontal em telas estreitas.
Para uma captura com título, quatro indicadores e dois gráficos completos,
use uma área de visualização de aproximadamente **1440 × 1000 pixels**.

Chart.js **4.4.9** está incluído em `dashboard/vendor/chart.umd.js`, com sua
licença MIT em `dashboard/vendor/LICENSE.md`; não há CDN em tempo de execução.
A origem dos arquivos está documentada em `dashboard/vendor/README.md`.

Validação opcional do dashboard no Chromium (não necessária para utilizá-lo):

```sh
python -m pip install playwright
python -m playwright install chromium
python -m unittest test_dashboard -v
```

Em Linux, o navegador de teste também requer suas bibliotecas de sistema;
o Playwright informa as dependências ausentes. Seis testes verificam os dados,
os indicadores, todos os valores dos gráficos, insights, tabelas, navegação
por teclado e larguras de 768, 390 e 320 pixels. O navegador roda offline e
os testes falham diante de erros no console ou solicitações HTTP(S).

Limites: a página mostra uma cópia estática dos resultados, sem atualização
automática de preços. A amostra é exclusivamente da KaBuM no momento da coleta;
grupos têm tamanhos e composições diferentes. Outliers IQR não são erros
comprovados. Os 17 modelos permanecem nos gráficos, inclusive grupos com uma
única observação. A execução desta etapa não realiza scraping nem publica o site.

## Análise preservada — etapa 5

## Análise local da amostra tratada

```sh
python analise.py
```

Lê exclusivamente `data/dados_tratados.csv`, valida a estrutura e calcula
caracterização, distribuição, agrupamentos por fabricante/modelo/família,
rankings, faixas de preço, outliers IQR e insights descritivos. Não consulta
a web, não modifica os CSVs e não remove outliers.

Os resultados são exibidos no terminal e gravados em
`data/resultados_analise.json`, com valores numéricos sem arredondamento
antecipado. A formatação monetária brasileira é apenas para apresentação.

Métodos: quartis com interpolação linear, desvio-padrão amostral (`ddof=1`)
e outliers estritamente fora de `[Q1 - 1,5 × IQR, Q3 + 1,5 × IQR]`.
As faixas usam limites superiores inclusivos, definidos após inspecionar a
base: 1.500, 3.000, 5.000, 8.000 e 12.000 reais, mais a faixa acima de 12.000.
O primeiro intervalo inclui preços positivos até 1.500 reais.

Para destacar variação dentro de modelos, o critério descritivo é ter pelo
menos duas ofertas, amplitude de ao menos R$ 1.000 e de ao menos 20% do menor
preço. Isso não representa significância estatística nem uma regra de compra.
Grupos com uma oferta são mantidos e sinalizados. Empates nos cinco menores
ou maiores preços preservam a ordem da base, mantendo cinco itens.

Execução validada: 86 produtos, média de R$ 4.909,43, mediana de R$ 4.299,99,
sete outliers superiores e nenhum inferior. O JSON inclui quatro insights
gerados dos resultados, as tabelas completas e os nomes/URLs dos produtos.

A amostra é apenas da KaBuM no momento da coleta. Diferenças de composição
impedem interpretar médias como um efeito isolado de marca. Um modelo de GPU
pode reunir placas com memória e construção diferentes. Não há conclusões
sobre todo o mercado, causalidade ou desempenho das placas.

Sete testes da análise, sem rede:

```sh
python -m unittest test_analise -v
```

As instruções abaixo documentam o pré-processamento e a coleta já existentes;
não é necessário executá-los novamente para analisar o CSV tratado atual.

## Pré-processamento preservado — etapa 4

Pré-processamento local de `data/dados_brutos.csv`, gerando separadamente
`data/dados_tratados.csv`. O tratamento não consulta a web nem altera o bruto.

Resultado validado: 89 registros de entrada, 86 tratados e oito colunas.
A inspeção encontrou três acessórios na categoria de placas de vídeo; eles
foram removidos apenas da base tratada. Cinco nomes tinham espaços repetidos.
Não foram encontrados valores essenciais ausentes, preços inválidos ou duplicatas.

## Executar o tratamento

Com as dependências de `requirements.txt` instaladas, execute na raiz:

```sh
python tratamento.py
```

Não é necessário executar `main.py` antes: ele faz uma nova coleta e substitui
o CSV bruto. Nesta etapa, o tratamento utiliza o arquivo já existente.

`tratamento.py` apresenta o diagnóstico, limpa espaços de forma conservadora,
converte preços para `float`, valida URLs e remove registros inutilizáveis e
duplicados. As três colunas derivadas são `fabricante`, `modelo_gpu` e
`familia_gpu`. Casos desconhecidos ou conflitantes recebem `Não identificado`.
O SHA-256 do bruto é conferido antes da gravação do tratado.

Regras relevantes:

- Preços com ponto decimal e preços brasileiros como `R$ 2.799,90` são aceitos.
  Valores ambíguos como `2.799` sem símbolo monetário, parcelas, zero, negativos
  e valores não finitos são rejeitados; nenhum inválido é substituído por zero.
- Nomes mantêm grafia, caixa, acentos e códigos. Somente espaços repetidos,
  quebras de linha e caracteres invisíveis definidos no código são limpos.
- URLs perdem apenas espaços externos; parâmetros são mantidos. A primeira
  ocorrência utilizável de cada URL é preservada, sem deduplicar por nome.
- Acessórios observados são identificados por nomes iniciados em `Suporte` ou
  `Cabo`; essa regra é limitada e não pretende classificar qualquer catálogo.
- Marcas são reconhecidas por palavras completas, sem diferenciar maiúsculas,
  usando somente fabricantes observados. São marcas da placa, não do chip GPU.
- Modelos usam expressões regulares para RTX/GTX, RX e Arc B; famílias seguem
  seus prefixos. As regras refletem os nomes da amostra atual.

O arquivo tratado tem as cinco colunas originais mais os três atributos derivados.
Na execução validada, os 86 registros tiveram atributos identificados: 12 marcas,
17 modelos e sete famílias distintos. Não foram calculados preços médios,
rankings ou outras análises. Não há gráficos nem Data Mining nesta etapa.

Verificações locais (dez testes, sem rede):

```sh
python -m unittest test_tratamento -v
```

## Coleta preservada — etapa 3

Coleta automática de até 100 ofertas disponíveis de placas de vídeo vendidas
pela própria KaBuM. A amostra aceita diferentes linhas e fabricantes, sem a
restrição anterior à RTX série 50.

Nesta etapa, `main.py` consulta apenas a KaBuM. O scraper da Amazon e os
relatórios das investigações anteriores continuam preservados, sem execução.

Execução validada da etapa 3: 89 registros salvos após cinco páginas e 300
registros examinados. Foram descartadas 211 ofertas de outros vendedores.
O CSV foi conferido contra as respostas da coleta; três páginas de produto
responderam HTTP 200 e confirmaram os nomes e preços da amostra verificada.
Na inspeção completa da etapa 4, foram encontrados três acessórios que a
categoria da fonte havia incluído como placas. Os scrapers não foram alterados
nesta etapa, e esses registros continuam preservados no arquivo bruto.

## Executar uma nova coleta (opcional, independente do tratamento)

Com Python 3.10 ou superior, a partir da raiz do repositório:

```sh
python -m venv .venv
```

Ative com `source .venv/bin/activate` no Linux/macOS ou
`.venv\Scripts\Activate.ps1` no PowerShell. Depois:

```sh
python -m pip install -r requirements.txt
python main.py
```

Se o Linux disponibilizar apenas `python3`, use-o para criar o ambiente.
O CSV é salvo em `data/dados_brutos.csv`, relativo à pasta do programa.
Uma execução com ofertas válidas substitui o CSV anterior. Se nenhuma oferta
for coletada, o programa retorna código 1 e preserva o arquivo existente.
Falhas depois de uma página válida são informadas no terminal; os registros
já coletados podem ser salvos. Uma amostra menor que 60 ofertas gera um aviso.

## KaBuM — fonte e mecanismo observado

- Fonte: https://www.kabum.com.br/hardware/placa-de-video-vga
- Parâmetros de paginação: `page_number` e `page_size=60`.
- Seletor BeautifulSoup: `script#__NEXT_DATA__[type="application/json"]`.
- Produtos: `props.pageProps.data.catalogServer.data`. Na categoria,
  `pageProps.data` pode ser texto JSON e é decodificado antes de acessar
  `catalogServer`; a leitura também continua aceitando um objeto, como na busca.
- Campos: `name`, `priceWithDiscount`, `offer.priceWithDiscount`, `code` e
  `friendlyName`.
- URL: `https://www.kabum.com.br/produto/{code}/{friendlyName}`,
  estrutura também observada nas ofertas do `script#productSchema`.
- Próxima página: `props.pageProps.data.catalogServer.pagination.next`.

O HTML inspecionado contém os dados em JSON, enquanto os cartões visuais
ainda são espaços de carregamento. Não são necessários Selenium, execução
de JavaScript ou chamadas a uma API interna.

O preço à vista em BRL é mantido na representação original do JSON, por
exemplo `2799.99`, sem conversão para número ou formatação monetária.
Os nomes também são preservados. `loja` e `categoria` são constantes
previstas no enunciado. Não há limpeza, análise ou preenchimento manual.

A categoria distingue preço regular e promoção: `offer.priceWithDiscount`
é escolhido quando a promoção está dentro de `startsAt`/`endsAt`, tem
`quantityAvailable > 0` e não é exclusiva de Prime ou de usuário autenticado.
Nos demais casos, usa-se `priceWithDiscount`. Nenhum desconto é calculado.
Uma promoção selecionada sem preço válido faz o registro ser ignorado.

A seleção confere a categoria `Placa de vídeo (VGA)`, o vendedor `KaBuM!`,
a disponibilidade e os campos mínimos. A restrição de modelo RTX 50 foi
removida. Ofertas de marketplace são ignoradas para que `loja = KaBuM`
represente o vendedor real.
URLs já coletadas não são repetidas ao percorrer páginas.

A coleta encerra ao alcançar 100 ofertas, ao acabar a paginação ou após
cinco páginas. O contador de encontrados corresponde aos registros
examinados até a parada. Válidos e ignorados somam esse contador.
O contador de páginas inclui cada requisição de catálogo tentada.
O timeout é de 30 segundos e o intervalo entre páginas é de um segundo.
Falhas HTTP ou mudanças na estrutura são informadas no terminal; a função
da KaBuM devolve ofertas já coletadas, se houver, mesmo após falha numa página.
O mecanismo de requisição, seletor, paginação e escrita de valores brutos
da etapa 1 foi mantido, com os ajustes de escopo e leitura da categoria.

## Amazon — implementação anterior, fora da execução atual

A investigação inicial retornou HTTP 200; a execução conjunta posterior
retornou HTTP 503 da Amazon e não gerou um CSV combinado. O arquivo
`scraper_amazon.py` foi preservado e não é importado por `main.py` nesta etapa.
As informações abaixo documentam essa implementação anterior.

- Fonte: https://www.amazon.com.br/s?k=placa+de+video+RTX
- Resposta investigada: HTTP 200, com 48 cartões diretamente no HTML.
- Scraper independente: `scraper_amazon.py`.
- Produto: `div[data-component-type="s-search-result"]`.
- Nome: `[data-cy="title-recipe"] h2`, conteúdo textual original.
- URL: `[data-cy="title-recipe"] a[href]`, convertida em absoluta com `urljoin`.
- Preço: primeiro `[data-cy="price-recipe"] .a-price:not(.a-text-price) .a-offscreen`.
- Próxima página: atributo `href` de `a.s-pagination-next[href]`.
- Identificador: `data-asin`, utilizado para evitar repetir produtos entre páginas.

O preço escolhido é o principal exibido no cartão. Pode representar Pix/NuPay
ou o preço normal, conforme a oferta; não representa a parcela nem o preço
riscado. O texto é preservado, incluindo `R$`, vírgulas, pontos e espaços.
Os valores da Amazon e da KaBuM não são normalizados.

A busca da Amazon é mais ampla que a da KaBuM: inclui placas de outras séries
e pode incluir seminovos. O filtro utiliza termos de placa de vídeo/GPU no
nome e exclui notebooks, computadores, cabos, suportes, adaptadores e outros
componentes claramente incompatíveis. Isso seleciona ofertas da categoria,
sem estabelecer equivalência de modelos ou condições entre as lojas.

`loja = Amazon` representa a fonte da coleta, não o vendedor. Há ofertas de
marketplace. O HTML inspecionado contém identificadores de vendedor em alguns
cartões, mas eles não foram convertidos em nomes nem adicionados ao CSV.

A coleta para ao atingir 30 ofertas ou após até três páginas, com intervalo
de um segundo entre páginas. O link de próxima página é seguido como fornecido
pelo site. Os contadores correspondem apenas aos cartões examinados até a parada.
Itens sem preço principal entram em informações ausentes; sua indisponibilidade
não é presumida. Não são buscados preços alternativos em páginas de produto.

Uma resposta HTTP de erro, CAPTCHA, verificação ou estrutura não reconhecida
interrompe a coleta da Amazon. Não há Selenium, proxies, cookies externos,
tentativas de resolver desafios ou repetição automática de requisições bloqueadas.
O acesso e os preços podem variar entre execuções e conforme o local de entrega
assumido pelo site; nenhum CEP é definido pelo scraper.

## Arquivos e saída

`main.py` executa a coleta ampliada da KaBuM, exibe as ofertas, as páginas,
os contadores de examinados e descartes e o total salvo. O arquivo
`data/dados_brutos.csv` mantém as mesmas cinco colunas:
`nome_produto`, `preco`, `loja`, `url`, `categoria`.
Não foram adicionadas dependências nem etapas de análise ou tratamento.
