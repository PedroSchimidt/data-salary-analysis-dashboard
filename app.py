import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Salary Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Salary Analytics — Carreiras em Dados")
st.caption("Dashboard para análise de salários na área de dados.")


@st.cache_data
def load_data():
    return pd.read_csv(
        "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
    )

df = load_data()

st.sidebar.title("⚙️ Configurações da Análise")

anos = sorted(df["ano"].unique())
senioridades = sorted(df["senioridade"].unique())

anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)
senior_sel = st.sidebar.multiselect(
    "Senioridade", senioridades, default=senioridades
)

st.sidebar.title("⚙️ Configurações da Análise")

anos = sorted(df["ano"].unique())
senioridades = sorted(df["senioridade"].unique())

anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)
senior_sel = st.sidebar.multiselect(
    "Senioridade", senioridades, default=senioridades
)

df_filtrado = df.query(
    "ano in @anos_sel and senioridade in @senior_sel"
)

media_filtro = df_filtrado["usd"].mean()
media_global = df["usd"].mean()
diferenca = media_filtro - media_global

col1, col2 = st.columns(2)

col1.metric("Salário médio (USD)", f"${media_filtro:,.0f}")
col2.metric("Média global (USD)", f"${media_global:,.0f}")