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

# ABAS

tab1, tab2, tab3 = st.tabs(
    ["📈 Análises Salariais", "🌍 Distribuição Geográfica", "📄 Base de Dados"]
)

# - TAB 1
with tab1:
    col_a, col_b = st.columns(2)

    if not df_filtrado.empty:
        top_cargos = (
            df_filtrado.groupby("cargo")["usd"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig_bar = px.bar(
            top_cargos,
            x="usd",
            y="cargo",
            orientation="h",
            title="Top 10 cargos por salário médio",
            labels={"usd": "Salário médio anual (USD)", "cargo": ""}
        )
        fig_bar.update_layout(yaxis=dict(autorange="reversed"))
        col_a.plotly_chart(fig_bar, use_container_width=True)

        fig_hist = px.histogram(
            df_filtrado,
            x="usd",
            nbins=35,
            title="Distribuição salarial",
            labels={"usd": "Salário anual (USD)"}
        )
        col_b.plotly_chart(fig_hist, use_container_width=True)

    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")

# - TAB 2
with tab2:
    if not df_filtrado.empty:
        remoto = df_filtrado["remoto"].value_counts().reset_index()
        remoto.columns = ["Modelo", "Quantidade"]

        fig_pie = px.pie(
            remoto,
            names="Modelo",
            values="Quantidade",
            hole=0.45,
            title="Modelo de trabalho"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
        if not df_ds.empty:

            st.info(
                "ℹ️ Países exibidos em branco no mapa indicam ausência de dados "
                "para o perfil selecionado."
            )

            mapa = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()

            fig_map = px.choropleth(
                mapa,
                locations="residencia_iso3",
                color="usd",
                title="Salário médio de Data Scientists por país",
                labels={"usd": "USD"}
            )
            st.plotly_chart(fig_map, use_container_width=True)
