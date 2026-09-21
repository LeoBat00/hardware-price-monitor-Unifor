# Monitoramento de preços — etapa 2

Coleta automática de até 30 ofertas de placas de vídeo por fonte: KaBuM e
Amazon Brasil. Somente coleta, terminal e armazenamento bruto em um CSV combinado.

Estado da validação: a investigação da Amazon retornou HTTP 200 e permitiu
implementar a extração. Na execução conjunta seguinte, a Amazon retornou
HTTP 503; a KaBuM coletou 30 ofertas, mas o CSV combinado não foi gerado.
A implementação da segunda fonte ainda depende de validação completa com
acesso normal à Amazon. O CSV existente continua sendo da etapa 1.

## Executar

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
Uma execução com ofertas válidas das duas fontes substitui o CSV anterior.
Se uma fonte não fornecer ofertas ou a Amazon apresentar erro/bloqueio, o
programa informa o problema, retorna código 1 e preserva o CSV anterior.

## KaBuM — fonte e mecanismo observado

- Fonte: https://www.kabum.com.br/busca/rtx-50
- Parâmetros de paginação: `page_number` e `page_size=60`.
- Seletor BeautifulSoup: `script#__NEXT_DATA__[type="application/json"]`.
- Produtos: `props.pageProps.data.catalogServer.data`.
- Campos: `name`, `priceWithDiscount`, `code` e `friendlyName`.
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

A busca inclui outros produtos e vendedores de marketplace; eles são
ignorados para que `loja = KaBuM` represente o vendedor real. A seleção
confere categoria, modelo RTX 50, vendedor, disponibilidade e campos mínimos.
URLs já coletadas não são repetidas ao percorrer páginas.

A coleta encerra ao alcançar 30 ofertas, ao acabar a paginação ou após
cinco páginas. O contador de encontrados corresponde aos registros
examinados até a parada. Válidos e ignorados somam esse contador.
Falhas HTTP ou mudanças na estrutura são informadas no terminal; a função
da KaBuM devolve ofertas já coletadas, se houver, mesmo após falha numa página.
Essa lógica da etapa 1 foi preservada integralmente em `scraper.py`.

## Amazon — fonte e mecanismo observado

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

`main.py` coordena as duas funções, exibe as ofertas e os contadores por fonte
e salva `data/dados_brutos.csv` com as mesmas cinco colunas:
`nome_produto`, `preco`, `loja`, `url`, `categoria`.
Não foram adicionadas dependências nem etapas de análise ou tratamento.
