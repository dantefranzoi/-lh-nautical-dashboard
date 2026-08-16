# LH Nautical — Dashboard Executivo

Dashboard interativo desenvolvido em Python (Streamlit) como material complementar do desafio técnico de dados da LH Nautical, empresa fictícia de varejo náutico.

## O que este dashboard mostra

O projeto responde cinco perguntas centrais de negócio, uma por página:

1. **Confiança** — Podemos confiar nesses dados para tomar decisões?
2. **Clientes** — Quem são nossos clientes mais valiosos?
3. **Operação** — Vale a pena fechar a loja em algum dia da semana?
4. **Previsão** — Quanto podemos vender nos próximos meses?
5. **Recomendações** — O que devemos recomendar na vitrine?

Cada página cruza os dados brutos (pedidos, itens, produtos, categorias e clientes) com as análises feitas ao longo do desafio: EDA, SQL, análise de clientes, calendário de vendas, previsão de demanda por média móvel e sistema de recomendação por similaridade de cosseno.

## Tecnologias

- **Python**
- **Streamlit** — interface do dashboard
- **Pandas** — manipulação dos dados
- **Plotly** — gráficos interativos

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Autor

Feito por Dante.
