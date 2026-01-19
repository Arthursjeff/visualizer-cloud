import pandas as pd
import streamlit as st

URL_BASE = (
    "https://raw.githubusercontent.com/Arthursjeff/"
    "visualizer-data/main/base_historica.csv"
)

@st.cache_data(ttl=60)
def carregar_base():
    df = pd.read_csv(URL_BASE)

    # Datas corretas da nova base
    if "data_orcamento_dt" in df.columns:
        df["data_orcamento_dt"] = pd.to_datetime(
            df["data_orcamento_dt"], errors="coerce"
        )

    if "data_pedido_dt" in df.columns:
        df["data_pedido_dt"] = pd.to_datetime(
            df["data_pedido_dt"], errors="coerce"
        )

    if "data_faturamento_dt" in df.columns:
        df["data_faturamento_dt"] = pd.to_datetime(
            df["data_faturamento_dt"], errors="coerce"
        )

    if "snapshot_dt" in df.columns:
        df["snapshot_dt"] = pd.to_datetime(
            df["snapshot_dt"], errors="coerce"
        )

    return df
