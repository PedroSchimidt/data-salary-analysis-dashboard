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