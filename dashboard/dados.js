// Gerado por preparar_dashboard.py. Não editar manualmente.
const dadosAnalise = {
  "metodologia": {
    "fonte": "data/dados_tratados.csv",
    "loja": "KaBuM",
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
      "Não há medidas de desempenho, histórico de preços ou dados de outras lojas."
    ]
  },
  "validacao": {
    "colunas": [
      "nome_produto",
      "preco",
      "loja",
      "url",
      "categoria",
      "fabricante",
      "modelo_gpu",
      "familia_gpu"
    ],
    "tipo_preco": "float64",
    "fabricantes_distintos": 12,
    "modelos_distintos": 17,
    "familias_distintas": 7,
    "sha256_entrada": "6f757f7c94761e899ff0cffe8c4f33ea6dc4b35a6331a605ce55412ffa1c9b58"
  },
  "resumo": {
    "quantidade": 86,
    "preco_medio": 4909.431279069766,
    "mediana": 4299.99,
    "preco_minimo": 1349.99,
    "preco_maximo": 15999.99
  },
  "distribuicao": {
    "q1": 2799.99,
    "q3": 5874.99,
    "iqr": 3075.0,
    "desvio_padrao": 3182.4436007991962,
    "limite_inferior": -1812.5100000000002,
    "limite_superior": 10487.49
  },
  "por_fabricante": [
    {
      "fabricante": "MSI",
      "quantidade": 21,
      "preco_medio": 5134.271904761905,
      "mediana": 3099.99,
      "preco_minimo": 1369.99,
      "preco_maximo": 13999.99
    },
    {
      "fabricante": "Gigabyte",
      "quantidade": 18,
      "preco_medio": 4239.990555555556,
      "mediana": 3299.99,
      "preco_minimo": 2299.99,
      "preco_maximo": 12000.0
    },
    {
      "fabricante": "ASUS",
      "quantidade": 12,
      "preco_medio": 5791.41,
      "mediana": 5299.99,
      "preco_minimo": 1399.99,
      "preco_maximo": 13999.99
    },
    {
      "fabricante": "Palit",
      "quantidade": 8,
      "preco_medio": 5641.8625,
      "mediana": 5042.48,
      "preco_minimo": 2799.99,
      "preco_maximo": 11999.99
    },
    {
      "fabricante": "ASRock",
      "quantidade": 5,
      "preco_medio": 4223.99,
      "mediana": 4799.99,
      "preco_minimo": 1919.99,
      "preco_maximo": 5899.99
    },
    {
      "fabricante": "PowerColor",
      "quantidade": 5,
      "preco_medio": 5615.99,
      "mediana": 5579.99,
      "preco_minimo": 3999.99,
      "preco_maximo": 6899.99
    },
    {
      "fabricante": "XFX",
      "quantidade": 5,
      "preco_medio": 6039.99,
      "mediana": 6999.99,
      "preco_minimo": 4599.99,
      "preco_maximo": 6999.99
    },
    {
      "fabricante": "Husky",
      "quantidade": 3,
      "preco_medio": 2166.6566666666663,
      "mediana": 2399.99,
      "preco_minimo": 1599.99,
      "preco_maximo": 2499.99
    },
    {
      "fabricante": "Inno3D",
      "quantidade": 3,
      "preco_medio": 7033.323333333334,
      "mediana": 3099.99,
      "preco_minimo": 1999.99,
      "preco_maximo": 15999.99
    },
    {
      "fabricante": "Galax",
      "quantidade": 2,
      "preco_medio": 1894.9899999999998,
      "mediana": 1894.9899999999998,
      "preco_minimo": 1489.99,
      "preco_maximo": 2299.99
    },
    {
      "fabricante": "PCYes",
      "quantidade": 2,
      "preco_medio": 1674.99,
      "mediana": 1674.99,
      "preco_minimo": 1349.99,
      "preco_maximo": 1999.99
    },
    {
      "fabricante": "PNY",
      "quantidade": 2,
      "preco_medio": 4649.99,
      "mediana": 4649.99,
      "preco_minimo": 2299.99,
      "preco_maximo": 6999.99
    }
  ],
  "por_modelo": [
    {
      "modelo_gpu": "RTX 5070",
      "quantidade": 14,
      "preco_medio": 6467.847857142857,
      "mediana": 5799.99,
      "preco_minimo": 5099.99,
      "preco_maximo": 12000.0,
      "amplitude": 6900.01,
      "amplitude_percentual": 135.29457900897845,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 5060",
      "quantidade": 13,
      "preco_medio": 2953.913846153846,
      "mediana": 2799.99,
      "preco_minimo": 2699.99,
      "preco_maximo": 3701.0,
      "amplitude": 1001.0100000000002,
      "amplitude_percentual": 37.07458175771022,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 5060 Ti",
      "quantidade": 13,
      "preco_medio": 4236.683076923076,
      "mediana": 4699.99,
      "preco_minimo": 3059.99,
      "preco_maximo": 6132.01,
      "amplitude": 3072.0200000000004,
      "amplitude_percentual": 100.39313853966844,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 5050",
      "quantidade": 8,
      "preco_medio": 2637.99125,
      "mediana": 2549.99,
      "preco_minimo": 2299.99,
      "preco_maximo": 3204.0,
      "amplitude": 904.0100000000002,
      "amplitude_percentual": 39.30495349979784,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RX 9070 XT",
      "quantidade": 8,
      "preco_medio": 6434.99,
      "mediana": 6749.99,
      "preco_minimo": 5499.99,
      "preco_maximo": 6999.99,
      "amplitude": 1500.0,
      "amplitude_percentual": 27.272776859594288,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 3050",
      "quantidade": 7,
      "preco_medio": 1494.2757142857142,
      "mediana": 1399.99,
      "preco_minimo": 1349.99,
      "preco_maximo": 1999.99,
      "amplitude": 650.0,
      "amplitude_percentual": 48.148504803739286,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 5080",
      "quantidade": 5,
      "preco_medio": 13639.972,
      "mediana": 13999.99,
      "preco_minimo": 11999.99,
      "preco_maximo": 15999.99,
      "amplitude": 4000.0,
      "amplitude_percentual": 33.33336111113426,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 5070 Ti",
      "quantidade": 4,
      "preco_medio": 10149.99,
      "mediana": 9999.99,
      "preco_minimo": 8599.99,
      "preco_maximo": 11999.99,
      "amplitude": 3400.0,
      "amplitude_percentual": 39.534929691778714,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RX 9060 XT",
      "quantidade": 3,
      "preco_medio": 4666.656666666667,
      "mediana": 4999.99,
      "preco_minimo": 3999.99,
      "preco_maximo": 4999.99,
      "amplitude": 1000.0,
      "amplitude_percentual": 25.00006250015625,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RX 9070",
      "quantidade": 3,
      "preco_medio": 4666.656666666667,
      "mediana": 4599.99,
      "preco_minimo": 4599.99,
      "preco_maximo": 4799.99,
      "amplitude": 200.0,
      "amplitude_percentual": 4.347835538772911,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "RTX 3060",
      "quantidade": 2,
      "preco_medio": 2459.99,
      "mediana": 2459.99,
      "preco_minimo": 2419.99,
      "preco_maximo": 2499.99,
      "amplitude": 80.0,
      "amplitude_percentual": 3.305798784292498,
      "multiplas_ofertas": true
    },
    {
      "modelo_gpu": "Arc B580",
      "quantidade": 1,
      "preco_medio": 2999.99,
      "mediana": 2999.99,
      "preco_minimo": 2999.99,
      "preco_maximo": 2999.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    },
    {
      "modelo_gpu": "GTX 1660 SUPER",
      "quantidade": 1,
      "preco_medio": 1999.99,
      "mediana": 1999.99,
      "preco_minimo": 1999.99,
      "preco_maximo": 1999.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    },
    {
      "modelo_gpu": "RTX 3060 Ti",
      "quantidade": 1,
      "preco_medio": 2399.99,
      "mediana": 2399.99,
      "preco_minimo": 2399.99,
      "preco_maximo": 2399.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    },
    {
      "modelo_gpu": "RX 580",
      "quantidade": 1,
      "preco_medio": 1599.99,
      "mediana": 1599.99,
      "preco_minimo": 1599.99,
      "preco_maximo": 1599.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    },
    {
      "modelo_gpu": "RX 7600",
      "quantidade": 1,
      "preco_medio": 1919.99,
      "mediana": 1919.99,
      "preco_minimo": 1919.99,
      "preco_maximo": 1919.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    },
    {
      "modelo_gpu": "RX 9050",
      "quantidade": 1,
      "preco_medio": 2499.99,
      "mediana": 2499.99,
      "preco_minimo": 2499.99,
      "preco_maximo": 2499.99,
      "amplitude": 0.0,
      "amplitude_percentual": 0.0,
      "multiplas_ofertas": false
    }
  ],
  "por_familia": [
    {
      "familia_gpu": "RTX 50",
      "quantidade": 57,
      "preco_medio": 5507.568070175439,
      "mediana": 4799.99,
      "preco_minimo": 2299.99,
      "preco_maximo": 15999.99
    },
    {
      "familia_gpu": "RX 9000",
      "quantidade": 15,
      "preco_medio": 5465.323333333333,
      "mediana": 5499.99,
      "preco_minimo": 2499.99,
      "preco_maximo": 6999.99
    },
    {
      "familia_gpu": "RTX 30",
      "quantidade": 10,
      "preco_medio": 1777.9899999999998,
      "mediana": 1469.99,
      "preco_minimo": 1349.99,
      "preco_maximo": 2499.99
    },
    {
      "familia_gpu": "Arc B",
      "quantidade": 1,
      "preco_medio": 2999.99,
      "mediana": 2999.99,
      "preco_minimo": 2999.99,
      "preco_maximo": 2999.99
    },
    {
      "familia_gpu": "GTX 16",
      "quantidade": 1,
      "preco_medio": 1999.99,
      "mediana": 1999.99,
      "preco_minimo": 1999.99,
      "preco_maximo": 1999.99
    },
    {
      "familia_gpu": "RX 500",
      "quantidade": 1,
      "preco_medio": 1599.99,
      "mediana": 1599.99,
      "preco_minimo": 1599.99,
      "preco_maximo": 1599.99
    },
    {
      "familia_gpu": "RX 7000",
      "quantidade": 1,
      "preco_medio": 1919.99,
      "mediana": 1919.99,
      "preco_minimo": 1919.99,
      "preco_maximo": 1919.99
    }
  ],
  "destaques_modelos": {
    "mais_ofertas": [
      {
        "modelo_gpu": "RTX 5070",
        "quantidade": 14,
        "preco_medio": 6467.847857142857,
        "mediana": 5799.99,
        "preco_minimo": 5099.99,
        "preco_maximo": 12000.0,
        "amplitude": 6900.01,
        "amplitude_percentual": 135.29457900897845,
        "multiplas_ofertas": true
      }
    ],
    "maiores_amplitudes": [
      {
        "modelo_gpu": "RTX 5070",
        "quantidade": 14,
        "preco_medio": 6467.847857142857,
        "mediana": 5799.99,
        "preco_minimo": 5099.99,
        "preco_maximo": 12000.0,
        "amplitude": 6900.01,
        "amplitude_percentual": 135.29457900897845,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5080",
        "quantidade": 5,
        "preco_medio": 13639.972,
        "mediana": 13999.99,
        "preco_minimo": 11999.99,
        "preco_maximo": 15999.99,
        "amplitude": 4000.0,
        "amplitude_percentual": 33.33336111113426,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5070 Ti",
        "quantidade": 4,
        "preco_medio": 10149.99,
        "mediana": 9999.99,
        "preco_minimo": 8599.99,
        "preco_maximo": 11999.99,
        "amplitude": 3400.0,
        "amplitude_percentual": 39.534929691778714,
        "multiplas_ofertas": true
      }
    ],
    "variacao_relevante": [
      {
        "modelo_gpu": "RTX 5070",
        "quantidade": 14,
        "preco_medio": 6467.847857142857,
        "mediana": 5799.99,
        "preco_minimo": 5099.99,
        "preco_maximo": 12000.0,
        "amplitude": 6900.01,
        "amplitude_percentual": 135.29457900897845,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5080",
        "quantidade": 5,
        "preco_medio": 13639.972,
        "mediana": 13999.99,
        "preco_minimo": 11999.99,
        "preco_maximo": 15999.99,
        "amplitude": 4000.0,
        "amplitude_percentual": 33.33336111113426,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5070 Ti",
        "quantidade": 4,
        "preco_medio": 10149.99,
        "mediana": 9999.99,
        "preco_minimo": 8599.99,
        "preco_maximo": 11999.99,
        "amplitude": 3400.0,
        "amplitude_percentual": 39.534929691778714,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5060 Ti",
        "quantidade": 13,
        "preco_medio": 4236.683076923076,
        "mediana": 4699.99,
        "preco_minimo": 3059.99,
        "preco_maximo": 6132.01,
        "amplitude": 3072.0200000000004,
        "amplitude_percentual": 100.39313853966844,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RX 9070 XT",
        "quantidade": 8,
        "preco_medio": 6434.99,
        "mediana": 6749.99,
        "preco_minimo": 5499.99,
        "preco_maximo": 6999.99,
        "amplitude": 1500.0,
        "amplitude_percentual": 27.272776859594288,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RTX 5060",
        "quantidade": 13,
        "preco_medio": 2953.913846153846,
        "mediana": 2799.99,
        "preco_minimo": 2699.99,
        "preco_maximo": 3701.0,
        "amplitude": 1001.0100000000002,
        "amplitude_percentual": 37.07458175771022,
        "multiplas_ofertas": true
      },
      {
        "modelo_gpu": "RX 9060 XT",
        "quantidade": 3,
        "preco_medio": 4666.656666666667,
        "mediana": 4999.99,
        "preco_minimo": 3999.99,
        "preco_maximo": 4999.99,
        "amplitude": 1000.0,
        "amplitude_percentual": 25.00006250015625,
        "multiplas_ofertas": true
      }
    ]
  },
  "faixas_preco": [
    {
      "faixa": "Até R$ 1.500,00",
      "limite_inferior_exclusivo": 0,
      "limite_superior_inclusivo": 1500,
      "quantidade": 6,
      "percentual": 6.976744186046512
    },
    {
      "faixa": "Acima de R$ 1.500,00 até R$ 3.000,00",
      "limite_inferior_exclusivo": 1500,
      "limite_superior_inclusivo": 3000,
      "quantidade": 26,
      "percentual": 30.23255813953488
    },
    {
      "faixa": "Acima de R$ 3.000,00 até R$ 5.000,00",
      "limite_inferior_exclusivo": 3000,
      "limite_superior_inclusivo": 5000,
      "quantidade": 22,
      "percentual": 25.581395348837212
    },
    {
      "faixa": "Acima de R$ 5.000,00 até R$ 8.000,00",
      "limite_inferior_exclusivo": 5000,
      "limite_superior_inclusivo": 8000,
      "quantidade": 21,
      "percentual": 24.418604651162788
    },
    {
      "faixa": "Acima de R$ 8.000,00 até R$ 12.000,00",
      "limite_inferior_exclusivo": 8000,
      "limite_superior_inclusivo": 12000,
      "quantidade": 7,
      "percentual": 8.13953488372093
    },
    {
      "faixa": "Acima de R$ 12.000,00",
      "limite_inferior_exclusivo": 12000,
      "limite_superior_inclusivo": null,
      "quantidade": 4,
      "percentual": 4.651162790697675
    }
  ],
  "mais_baratos": [
    {
      "nome_produto": "Placa de Vídeo PcYes Nvidia Geforce Rtx 3050 6Gb Gddr6 96Bits - Pvpcr30506Gb2F",
      "preco": 1349.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/998334/placa-de-video-pcyes-nvidia-geforce-rtx-3050-6gb-gddr6-96bits-pvpcr30506gb2f",
      "categoria": "Placa de vídeo",
      "fabricante": "PCYes",
      "modelo_gpu": "RTX 3050",
      "familia_gpu": "RTX 30"
    },
    {
      "nome_produto": "Placa De Vídeo MSI RTX 3050 LP OC NVIDIA Geforce, 6GB, GDDR6, 96-Bit, Low Profile - G3050LP6C",
      "preco": 1369.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/1012613/placa-de-video-msi-rtx-3050-lp-oc-nvidia-geforce-6gb-gddr6-96-bit-low-profile-g3050lp6c",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 3050",
      "familia_gpu": "RTX 30"
    },
    {
      "nome_produto": "Placa de Vídeo RTX 3050 ASUS 6G Dual OC NVIDIA GeForce, 6GB GDDR6, DLSS, Ray Tracing, G-Sync - 90YV0K60-M0NA00",
      "preco": 1399.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/520492/placa-de-video-rtx-3050-asus-6g-dual-oc-nvidia-geforce-6gb-gddr6-dlss-ray-tracing-g-sync-90yv0k60-m0na00",
      "categoria": "Placa de vídeo",
      "fabricante": "ASUS",
      "modelo_gpu": "RTX 3050",
      "familia_gpu": "RTX 30"
    },
    {
      "nome_produto": "Placa de Video MSI GeForce RTX 3050 Ventus OC 2X, 6GB, GDDR6, 96-bit, 912-V812-060",
      "preco": 1399.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/997881/placa-de-video-msi-geforce-rtx-3050-ventus-oc-2x-6gb-gddr6-96-bit-912-v812-060",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 3050",
      "familia_gpu": "RTX 30"
    },
    {
      "nome_produto": "Placa de Vídeo MSI RTX 3050 Ventus 2X OC NVIDIA GeForce, 6GB GDDR6, 96-bit - G3050V2X6C",
      "preco": 1449.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/1003726/placa-de-video-msi-rtx-3050-ventus-2x-oc-nvidia-geforce-6gb-gddr6-96-bit-g3050v2x6c",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 3050",
      "familia_gpu": "RTX 30"
    }
  ],
  "mais_caros": [
    {
      "nome_produto": "Placa de Vídeo Inno3D RTX 5080 X3 NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - N50803-16D7-176068N",
      "preco": 15999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/697891/placa-de-video-inno3d-rtx-5080-x3-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-n50803-16d7-176068n",
      "categoria": "Placa de vídeo",
      "fabricante": "Inno3D",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50"
    },
    {
      "nome_produto": "Placa de Vídeo MSI RTX 5080 16G GAMING TRIO OC NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - G5080-16GTC",
      "preco": 13999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/699603/placa-de-video-msi-rtx-5080-16g-gaming-trio-oc-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-g5080-16gtc",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50"
    },
    {
      "nome_produto": "Placa de Vídeo ASUS RTX 5080 TUF GAMING OC 16G NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - 90YV0M30-M0NA00",
      "preco": 13999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/690383/placa-de-video-asus-rtx-5080-tuf-gaming-oc-16g-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-90yv0m30-m0na00",
      "categoria": "Placa de vídeo",
      "fabricante": "ASUS",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50"
    },
    {
      "nome_produto": "Placa de Vídeo MSI GeForce RTX 5080 16G SHADOW 3X OC, 16GB GDDR7, 256 bits, NVIDIA® GeForce RTX? 5080 - G5080-16S3C",
      "preco": 12199.9,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/725585/placa-de-video-msi-geforce-rtx-5080-16g-shadow-3x-oc-16gb-gddr7-256-bits-nvidia-geforce-rtx-5080-g5080-16s3c",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50"
    },
    {
      "nome_produto": "Placa de Vídeo Gigabyte RTX 5070 GAMING OC 12G NVIDIA GeForce, 12GB GDDR7, 192bits, RGB, DLSS, Ray Tracing - 9VN5070GO-00-G10",
      "preco": 12000.0,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/714571/placa-de-video-gigabyte-rtx-5070-gaming-oc-12g-nvidia-geforce-12gb-gddr7-192bits-rgb-dlss-ray-tracing-9vn5070go-00-g10",
      "categoria": "Placa de vídeo",
      "fabricante": "Gigabyte",
      "modelo_gpu": "RTX 5070",
      "familia_gpu": "RTX 50"
    }
  ],
  "outliers": [
    {
      "nome_produto": "Placa de Vídeo Inno3D RTX 5080 X3 NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - N50803-16D7-176068N",
      "preco": 15999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/697891/placa-de-video-inno3d-rtx-5080-x3-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-n50803-16d7-176068n",
      "categoria": "Placa de vídeo",
      "fabricante": "Inno3D",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo MSI RTX 5080 16G GAMING TRIO OC NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - G5080-16GTC",
      "preco": 13999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/699603/placa-de-video-msi-rtx-5080-16g-gaming-trio-oc-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-g5080-16gtc",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo ASUS RTX 5080 TUF GAMING OC 16G NVIDIA GeForce, 16GB, GDDR7, G-Sync, Ray Tracing, DLSS 4, HDR - 90YV0M30-M0NA00",
      "preco": 13999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/690383/placa-de-video-asus-rtx-5080-tuf-gaming-oc-16g-nvidia-geforce-16gb-gddr7-g-sync-ray-tracing-dlss-4-hdr-90yv0m30-m0na00",
      "categoria": "Placa de vídeo",
      "fabricante": "ASUS",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo MSI GeForce RTX 5080 16G SHADOW 3X OC, 16GB GDDR7, 256 bits, NVIDIA® GeForce RTX? 5080 - G5080-16S3C",
      "preco": 12199.9,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/725585/placa-de-video-msi-geforce-rtx-5080-16g-shadow-3x-oc-16gb-gddr7-256-bits-nvidia-geforce-rtx-5080-g5080-16s3c",
      "categoria": "Placa de vídeo",
      "fabricante": "MSI",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo Gigabyte RTX 5070 GAMING OC 12G NVIDIA GeForce, 12GB GDDR7, 192bits, RGB, DLSS, Ray Tracing - 9VN5070GO-00-G10",
      "preco": 12000.0,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/714571/placa-de-video-gigabyte-rtx-5070-gaming-oc-12g-nvidia-geforce-12gb-gddr7-192bits-rgb-dlss-ray-tracing-9vn5070go-00-g10",
      "categoria": "Placa de vídeo",
      "fabricante": "Gigabyte",
      "modelo_gpu": "RTX 5070",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo Palit RTX 5080 GamingPro NVIDIA GeForce, 16GB, GDDR7, ARGB SYNC EVO, G-Sync, Ray Tracing, DLSS 4 - NE75080019T2-GB2031Y",
      "preco": 11999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/697757/placa-de-video-palit-rtx-5080-gamingpro-nvidia-geforce-16gb-gddr7-argb-sync-evo-g-sync-ray-tracing-dlss-4-ne75080019t2-gb2031y",
      "categoria": "Placa de vídeo",
      "fabricante": "Palit",
      "modelo_gpu": "RTX 5080",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    },
    {
      "nome_produto": "Placa de Vídeo Asus ROG STRIX RTX 5070 TI OC 16G GAMING NVIDIA Geforce, 16GB, GDDR7, 256bits, Triple Fan, DLSS 4 - 90YV0M90-M0NA00",
      "preco": 11999.99,
      "loja": "KaBuM",
      "url": "https://www.kabum.com.br/produto/761536/placa-de-video-asus-rog-strix-rtx-5070-ti-oc-16g-gaming-nvidia-geforce-16gb-gddr7-256bits-triple-fan-dlss-4-90yv0m90-m0na00",
      "categoria": "Placa de vídeo",
      "fabricante": "ASUS",
      "modelo_gpu": "RTX 5070 Ti",
      "familia_gpu": "RTX 50",
      "motivo": "acima do limite superior"
    }
  ],
  "insights": [
    "Na amostra da KaBuM, a faixa 'Acima de R$ 1.500,00 até R$ 3.000,00' reúne 26 de 86 ofertas (30.23%).",
    "Entre os modelos com pelo menos duas ofertas, RTX 5070 apresenta a maior amplitude: R$ 6.900,01, de R$ 5.099,99 a R$ 12.000,00, em 14 ofertas (135.29% do menor preço). As placas podem diferir em memória, construção e outras especificações não controladas.",
    "A família RTX 50 reúne 57 de 86 ofertas (66.28%), com mediana de R$ 4.799,99. Essa composição da amostra deve ser considerada ao interpretar a distribuição geral; não mede participação no mercado.",
    "Pelo IQR global, 7 ofertas estão fora dos limites: 7 acima de R$ 10.487,49 e 0 abaixo de R$ -1.812,51. São extremos da amostra, não erros comprovados; nenhum registro foi removido."
  ]
};
const textosGraficos = {
  "faixas": "Na amostra da KaBuM, a faixa 'Acima de R$ 1.500,00 até R$ 3.000,00' reúne 26 de 86 ofertas (30.23%).",
  "modelos": "Na amostra analisada, os primeiros modelos por quantidade são: RTX 5070 (14 ofertas); RTX 5060 (13 ofertas); RTX 5060 Ti (13 ofertas).",
  "medias": "As maiores médias entre os modelos da amostra são: RTX 5080 (R$ 13.639,97); RTX 5070 Ti (R$ 10.149,99). Um mesmo modelo pode reunir diferentes versões e capacidades de memória."
};
