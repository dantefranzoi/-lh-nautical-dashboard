import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

st.set_page_config(page_title="LH Nautical - Dashboard", page_icon="logo.png", layout="wide")

NAVY = "#002B5C"
DEEP = "#003B73"
MEDIUM = "#0077B6"
TEAL = "#19B5C9"
BEAM = "#8ED8E8"
WHITE = "#FFFFFF"
CINZA = "#7A8699"
CINZA_CLARO = "#D8E0E8"
ALERT = "#D6553F"
BG = "#F4F7FA"

FONT = "Arial, Helvetica, sans-serif"

st.markdown(f"""
<style>
.stApp {{ background-color: {BG}; font-family: {FONT}; }}
section[data-testid="stSidebar"] {{ background-color: {NAVY}; }}
section[data-testid="stSidebar"] label {{ color: white !important; }}
section[data-testid="stSidebar"] .stRadio p {{ color: white !important; font-size: 15px; }}
div[data-testid="stMetric"] {{
background-color: white;
border: 1px solid #E2E8EE;
border-left: 5px solid {TEAL};
border-radius: 12px;
padding: 14px 18px;
}}
div[data-testid="stMetric"] label {{ color: {CINZA}; font-weight: 600; }}
.card {{
background-color: white;
border: 1px solid #E2E8EE;
border-radius: 12px;
padding: 18px 20px;
min-height: 175px;
}}
.badge-periodo {{
background-color: #EFF3F7;
border-radius: 8px;
padding: 8px 14px;
font-size: 12px;
color: {NAVY};
display: inline-block;
}}
.insight-box {{ background-color: #E6F6F8; border-radius: 10px; padding: 16px 18px; }}
.insight-box b {{ color: {NAVY}; }}
.alert-box {{ background-color: #FBE4E0; border-radius: 10px; padding: 16px 18px; }}
.action-box {{ background-color: #E3F3E9; border-radius: 10px; padding: 16px 18px; }}
</style>
""", unsafe_allow_html=True)


def grafico_barra_h(labels, valores, cor_destaque_idx=None, formato="R$ {:,.0f}", altura=320):
    n = len(labels)
    cores = [CINZA_CLARO] * n
    if cor_destaque_idx is not None:
        cores[cor_destaque_idx] = TEAL
    textos = [formato.format(v) for v in valores]
    fig = go.Figure(go.Bar(
        x=valores, y=labels, orientation="h",
        marker_color=cores,
        text=textos, textposition="outside",
        textfont=dict(size=11, color=NAVY, family=FONT),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=altura,
        margin=dict(l=10, r=90, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family=FONT, color=NAVY, size=12),
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(type="category", categoryorder="array", categoryarray=labels,
                    showgrid=False, zeroline=False, tickfont=dict(size=12)),
        showlegend=False,
    )
    return fig


def grafico_barra_v(labels, valores, cor_destaque_idx=None, formato="R$ {:,.0f}", altura=340):
    n = len(labels)
    cores = [CINZA_CLARO] * n
    if cor_destaque_idx is not None:
        cores[cor_destaque_idx] = ALERT
    textos = [formato.format(v) for v in valores]
    fig = go.Figure(go.Bar(
        x=labels, y=valores,
        marker_color=cores,
        text=textos, textposition="outside",
        textfont=dict(size=11, color=NAVY, family=FONT),
        cliponaxis=False,
    ))
    fig.update_layout(
        height=altura,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family=FONT, color=NAVY, size=12),
        yaxis=dict(visible=False, showgrid=False, zeroline=False),
        xaxis=dict(type="category", showgrid=False, zeroline=False, tickfont=dict(size=12)),
        showlegend=False,
    )
    return fig


def grafico_dispersao(x, y, tamanhos, altura=340):
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers",
        marker=dict(size=tamanhos, sizemode="area",
                    sizeref=2.*max(tamanhos)/(38.**2), sizemin=6,
                    color=MEDIUM, opacity=0.75, line=dict(width=0)),
    ))
    fig.update_layout(
        height=altura,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family=FONT, color=NAVY, size=12),
        xaxis=dict(title="Frequência de compra (nº pedidos)", showgrid=True, gridcolor="#EEF2F6", zeroline=False),
        yaxis=dict(title="Faturamento total (R$)", showgrid=True, gridcolor="#EEF2F6", zeroline=False),
        showlegend=False,
    )
    return fig


def grafico_linha_previsao(meses, real, previsto, altura=340):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses, y=real, mode="lines", name="Vendas reais",
                              line=dict(color=NAVY, width=2)))
    fig.add_trace(go.Scatter(x=meses, y=previsto, mode="lines+markers", name="Previsão (média móvel)",
                              line=dict(color=TEAL, width=2, dash="dash"), marker=dict(size=6)))
    fig.add_vrect(x0="2026-01-01", x1="2026-03-31", fillcolor=BEAM, opacity=0.25, line_width=0,
                  annotation_text="período de teste", annotation_position="top left",
                  annotation_font=dict(size=10, color=NAVY))
    fig.update_layout(
        height=altura,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family=FONT, color=NAVY, size=12),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#EEF2F6", zeroline=False, title="unidades vendidas / mês"),
        legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11)),
    )
    return fig


with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = (
            "<div style='background-color:white; border-radius:12px; padding:14px 10px; "
            "width:170px; margin:0 auto 18px auto; text-align:center;'>"
            f"<img src='data:image/png;base64,{logo_b64}' style='width:100%;'>"
            "</div>"
        )
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.markdown("### LH NÁUTICA")
        st.caption("insights que guiam decisões")

    st.markdown("---")
    pagina = st.radio(
        "Navegação",
        ["01 · Confiança", "02 · Clientes", "03 · Operação", "04 · Previsão", "05 · Recomendações"],
        label_visibility="collapsed"
    )
    st.markdown(
        "<div style='position:fixed; bottom:18px; left:0; width:244px; "
        "text-align:center; color:#8FA3BD; font-size:12px; letter-spacing:1px;'>"
        "Feito por Dante</div>",
        unsafe_allow_html=True
    )

col_t, col_p = st.columns([3, 1])
with col_p:
    st.markdown("<div class='badge-periodo'>📅 Período analisado<br><b>01/01/2020 a 31/12/2026</b></div>", unsafe_allow_html=True)

if pagina.startswith("01"):
    with col_t:
        st.title("01 | Podemos confiar nesses dados?")
        st.caption("Qualidade e consistência da base de pedidos (orders)")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🛒 Total de pedidos", "48.998")
    c2.metric("📅 Período analisado", "2020 a 2026", "7 anos", delta_color="off")
    c3.metric("💰 Ticket médio", "R$ 28.704,99")
    c4.metric("📈 Maior venda", "R$ 127.262,02")

    st.markdown("#### Diagnóstico da base")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown("<div class='card'><b>✅ Qualidade dos dados</b><br><br>"
                     "Sem nulos em colunas essenciais<br>Sem pedidos duplicados<br>"
                     "Consistência aritmética de 100%</div>", unsafe_allow_html=True)
    with d2:
        st.markdown(f"<div class='card'><b>🔍 Valores nulos</b><br><br>"
                     f"Apenas em salesperson_id, esperado em pedidos de e-commerce<br><br>"
                     f"<span style='color:{TEAL}'><b>Impacto: BAIXO</b></span></div>", unsafe_allow_html=True)
    with d3:
        st.markdown(f"<div class='card'><b>📊 Outliers identificados</b><br><br>"
                     f"452 pedidos (0,9%) acima do padrão, compatíveis com itens de alto valor<br><br>"
                     f"<span style='color:{TEAL}'><b>Impacto: LEGÍTIMO</b></span></div>", unsafe_allow_html=True)
    with d4:
        st.markdown("<div class='card'><b>📆 Periodicidade</b><br><br>"
                     "Dados contínuos de jan/2020 a dez/2026, sem lacunas relevantes</div>", unsafe_allow_html=True)

    st.markdown(" ")
    st.success("Os dados apresentam consistência suficiente para sustentar as análises apresentadas neste dashboard.")

elif pagina.startswith("02"):
    with col_t:
        st.title("02 | Quem são nossos clientes mais valiosos?")
        st.caption("Análise dos clientes fiéis: ticket médio alto e 13 ou mais categorias distintas")

    clientes_labels = ["Marcela Câmara", "Henry Gabriel Viana", "Ana Laura Jesus", "Bárbara Albuquerque",
                        "Beatriz Garcia", "Ana Júlia Mendes", "Thomas Alves", "Mendes ME",
                        "Pedro Lucas da Conceição", "Isadora Rios"]
    clientes_vals = [39532.94, 39841.05, 39904.66, 40021.27, 40340.44, 40773.57, 40983.57, 41645.23, 41648.30, 41839.94]
    frequencia = [29, 17, 25, 26, 18, 20, 16, 26, 22, 26]
    faturamento = [1146455.22, 677297.78, 997616.46, 1040553.09, 726127.99, 815471.30, 655737.20, 1082775.89, 916262.58, 1087838.44]

    col1, col2 = st.columns([1.15, 1])
    with col1:
        st.markdown("**TOP 10 CLIENTES FIÉIS, POR TICKET MÉDIO**")
        st.plotly_chart(grafico_barra_h(clientes_labels, clientes_vals, cor_destaque_idx=9),
                         use_container_width=True, key="chart_top10")
    with col2:
        st.markdown("**FREQUÊNCIA DE COMPRA x FATURAMENTO TOTAL**")
        st.plotly_chart(grafico_dispersao(frequencia, faturamento, faturamento),
                         use_container_width=True, key="chart_scatter")

    col3, col4 = st.columns([1.3, 1])
    with col3:
        cat_labels = ["Iluminação", "Âncoras", "Eletrônica Náutica", "Coletes Salva-Vidas", "Hélices"]
        cat_vals = [7.6, 9.8, 11.7, 14.2, 18.6]
        st.markdown("**CATEGORIAS MAIS COMPRADAS POR ESSES CLIENTES**")
        st.plotly_chart(grafico_barra_h(cat_labels, cat_vals, cor_destaque_idx=4, formato="{:.1f}%"),
                         use_container_width=True, key="chart_categorias")
    with col4:
        st.markdown("<div class='insight-box'>⭐ <b>INSIGHT PRINCIPAL</b><br><br>"
                     "Os 10 clientes fiéis navegam uniformemente por <b>14 categorias distintas</b>. "
                     "Diversidade de compra, não volume isolado, é o que define fidelidade. "
                     "Categoria mais comprada: <b>Hélices</b> (492 itens).</div>", unsafe_allow_html=True)

elif pagina.startswith("03"):
    with col_t:
        st.title("03 | Vale a pena fechar a loja em algum dia?")
        st.caption("Média de vendas por dia da semana (loja física), considerando dias sem venda")

    dias_labels = ["Quinta", "Domingo", "Segunda", "Sábado", "Terça", "Sexta", "Quarta"]
    dias_vals = [157154.32, 157616.13, 158241.15, 164858.27, 166118.83, 170193.68, 173605.44]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**MÉDIA DE VENDAS POR DIA DA SEMANA, DO PIOR PARA O MELHOR**")
        st.plotly_chart(grafico_barra_v(dias_labels, dias_vals, cor_destaque_idx=0),
                         use_container_width=True, key="chart_dias")
    with col2:
        st.markdown("<div class='card'>ℹ️ <b>CONTEXTO</b><br><br>"
                     "O cálculo correto considera também os dias em que não houve venda, "
                     "evitando uma média artificialmente elevada.</div>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("<div class='alert-box'>⚠️ <b>INSIGHT</b><br><br>"
                     "Pior dia: <b>Quinta-feira</b><br>Média correta: <b>R$ 157.154,32</b><br><br>"
                     "O cálculo incorreto do estagiário, sem contar dias sem venda, apontava a "
                     "<b>Segunda-feira</b> como pior dia, R$ 161.335,26.<br><br>"
                     "A Quinta-feira tem <b>20 dias sem venda</b>, o dobro da Segunda-feira (7 dias).</div>", unsafe_allow_html=True)

    st.info("Quinta-feira é o dia com menor desempenho médio real. Avaliar ações para aumentar o movimento ou considerar redução de custo operacional nesse dia.")

elif pagina.startswith("04"):
    with col_t:
        st.title("04 | Quanto podemos vender nos próximos meses?")
        st.caption("Previsão de demanda, Média Móvel (baseline). Produto: Bússola de Bordo 702")

    serie = [29,16,17,28,5,8,4,9,16,0,56,45,16,24,28,20,14,7,0,11,3,23,40,45,13,24,33,23,0,15,0,12,17,70,21,49,19,33,22,44,0,5,6,4,21,33,45,42,33,43,56,44,28,13,5,10,10,20,47,18,53,32,58,38,24,17,14,23,26,25,54,19,76,55,51]
    meses = pd.date_range("2020-01-01", periods=len(serie), freq="MS")
    previsto = [None]*(len(serie)-4) + [19, 32.67, 49.67, 50.0]

    col1, col2 = st.columns([2.3, 1])
    with col1:
        st.markdown("**SÉRIE HISTÓRICA E PREVISÃO**")
        st.plotly_chart(grafico_linha_previsao(meses, serie, previsto),
                         use_container_width=True, key="chart_previsao")
    with col2:
        st.metric("MAE (erro médio absoluto)", "16,56", "unidades / mês", delta_color="off")
        st.markdown(" ")
        st.markdown("<div class='card'><b>SOBRE O MODELO</b><br><br>"
                     "Modelo simples de média móvel dos últimos 3 meses.<br><br>"
                     "Funciona bem para tendência estável, mas erra mais em meses de alta sazonalidade, "
                     "como o verão. Foi o que aconteceu em Jan/2026: previu 33, vendeu 76.</div>", unsafe_allow_html=True)

    st.info("A previsão fornece uma referência inicial para planejamento, mas ainda deve ser aprimorada para capturar sazonalidade antes de automatizar compras com fornecedores.")

else:
    with col_t:
        st.title("05 | O que devemos recomendar na vitrine?")
        st.caption("Recomendação de produtos com base em similaridade de comportamento de compra")

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("<div class='card'>⚓ <b>PRODUTO ANALISADO</b><br><br>"
                     f"<span style='font-size:20px; font-weight:700; color:{NAVY}'>Motor de Popa 1949</span></div>", unsafe_allow_html=True)
        st.markdown(" ")
        rec_labels = ["Vela Mestra 3870", "Motor de Popa 1540", "GPS Plotter 2249", "Cabo Náutico 2105", "Vela Mestra 1913"]
        rec_vals = [0.2088, 0.2121, 0.2148, 0.2300, 0.2452]
        st.markdown("**TOP 5 PRODUTOS RECOMENDADOS, POR SIMILARIDADE**")
        st.plotly_chart(grafico_barra_h(rec_labels, rec_vals, cor_destaque_idx=4, formato="{:.4f}"),
                         use_container_width=True, key="chart_recs")
    with col2:
        st.markdown("<div class='card'>🎯 <b>CRITÉRIO DE RECOMENDAÇÃO</b><br><br>"
                     "Similaridade de cosseno entre produtos, baseada em quais clientes compraram cada um, "
                     "não em categoria ou preço.</div>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("<div class='insight-box'>⭐ <b>INSIGHT PRINCIPAL</b><br><br>"
                     "O item mais similar não é outro motor, é a <b>Vela Mestra 1913</b>. "
                     "Isso mostra que a recomendação captura comportamento de compra real, "
                     "não apenas categoria parecida.</div>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("<div class='action-box'>✅ <b>AÇÃO SUGERIDA</b><br><br>"
                     "Exibir a Vela Mestra 1913 na vitrine \"quem comprou, também levou\" do Motor de Popa 1949 "
                     "para aumentar as vendas cruzadas.</div>", unsafe_allow_html=True)