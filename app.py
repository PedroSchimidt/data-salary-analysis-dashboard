import streamlit as st
import pandas as pd
import plotly.express as px


# CONFIGURAÇÃO GLOBAL

st.set_page_config(
    page_title="Salary Analytics | Data Careers",
    page_icon="📊",
    layout="wide"
)


# CARREGAMENTO DE DADOS (CACHE)

@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
    )
    return df

df = load_data()


# SIDEBAR - FILTROS

st.sidebar.title("⚙️ Configurações da Análise")
st.sidebar.markdown("Personalize os filtros para explorar diferentes cenários salariais.")

anos = sorted(df["ano"].unique())
senioridades = sorted(df["senioridade"].unique())
contratos = sorted(df["contrato"].unique())
tamanhos = sorted(df["tamanho_empresa"].unique())
cargos = sorted(df["cargo"].unique())

anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)
senior_sel = st.sidebar.multiselect("Senioridade", senioridades, default=senioridades)
contrato_sel = st.sidebar.multiselect("Tipo de contrato", contratos, default=contratos)
tamanho_sel = st.sidebar.multiselect("Tamanho da empresa", tamanhos, default=tamanhos)
cargo_sel = st.sidebar.multiselect("Cargo analisado", cargos, default=cargos)


# FILTRAGEM

df_filtrado = df.query(
    "ano in @anos_sel and senioridade in @senior_sel and contrato in @contrato_sel "
    "and tamanho_empresa in @tamanho_sel and cargo in @cargo_sel"
)


# HEADER

st.title("📊 Salary Analytics — Carreiras em Dados")
st.caption(
    "Dashboard analítico para exploração de salários globais na área de dados. "
    "Os insights são ajustados dinamicamente com base nos filtros selecionados."
)

st.markdown("---")


# KPIs + COMPARAÇÃO

st.subheader("📌 Resumo Executivo")

if not df_filtrado.empty:
    media_filtro = df_filtrado["usd"].mean()
    media_global = df["usd"].mean()
    diferenca = media_filtro - media_global
    registros = len(df_filtrado)
    cargo_destaque = df_filtrado["cargo"].mode()[0]
else:
    media_filtro = media_global = diferenca = registros = 0
    cargo_destaque = "-"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Salário médio (USD)",
    f"${media_filtro:,.0f}",
    delta=f"{diferenca:,.0f} vs média global"
)

col2.metric("Salário médio global", f"${media_global:,.0f}")
col3.metric("Total de registros", f"{registros:,}")
col4.metric("Cargo mais analisado", cargo_destaque)

# INSIGHT AUTOMÁTICO

if not df_filtrado.empty:
    if diferenca > 0:
        st.success(
            f"💡 Insight: Os filtros selecionados apresentam salários **acima da média global**, "
            f"com diferença média de ${diferenca:,.0f}."
        )

