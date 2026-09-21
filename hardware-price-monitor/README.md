# Monitoramento de preços — etapa 1

Coleta automática de até 30 ofertas disponíveis de placas RTX série 50,
vendidas pela própria KaBuM. Somente coleta, terminal e armazenamento bruto.

## Executar

Com Python 3.10 ou superior, a partir da raiz do repositório:

```sh
cd hardware-price-monitor
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
Uma execução com ofertas válidas substitui o CSV anterior.

## Fonte e mecanismo observado

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
Falhas HTTP ou mudanças na estrutura são informadas no terminal; ofertas
já coletadas são preservadas. Se nenhuma for válida, o programa termina
com código 1 e não sobrescreve um CSV anterior.
