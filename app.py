import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Dashboard Cripto", page_icon="📊", layout="wide")

# Título
st.title("📊 Dashboard de Criptomoedas")
st.markdown("Visualize dados em tempo real com a API da **CoinGecko**")

# Seleção de moeda base
moeda = st.selectbox("Selecione a moeda base:", ["usd", "eur", "brl"])

# Coleta de dados da API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": moeda,
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False,
}
data = requests.get(url, params=params).json()

# Transformar em DataFrame
df = pd.DataFrame(data)[
    ["id", "current_price", "market_cap", "price_change_percentage_24h"]
]
df.rename(
    columns={
        "id": "Criptomoeda",
        "current_price": f"Preço ({moeda.upper()})",
        "market_cap": "Market Cap",
        "price_change_percentage_24h": "Variação 24h (%)",
    },
    inplace=True,
)

# Layout em colunas
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Top 10 Criptomoedas")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Variação nas últimas 24h")
    fig = px.bar(
        df,
        x="Criptomoeda",
        y="Variação 24h (%)",
        color="Variação 24h (%)",
        text="Variação 24h (%)",
    )
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ Dados carregados em tempo real!")