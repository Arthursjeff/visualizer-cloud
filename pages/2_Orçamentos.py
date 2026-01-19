# ==========================================================
# ORÇAMENTOS
# ==========================================================

import streamlit as st
import pandas as pd
from utils import carregar_base

st.set_page_config(
    page_title="Orçamentos",
    layout="wide"
)

# ==========================================================
# CARREGAR BASE HISTÓRICA
# ==========================================================

df = carregar_base()

if df.empty:
    st.warning("Base histórica vazia.")
    st.stop()

# Garantir tipo datetime
df["data_orcamento_dt"] = pd.to_datetime(df["data_orcamento_dt"], errors="coerce")

# ==========================================================
# FILTROS
# ==========================================================

st.markdown("## Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    data_ini = st.date_input(
        "Data inicial",
        value=df["data_orcamento_dt"].min().date()
    )

with col2:
    data_fim = st.date_input(
        "Data final",
        value=df["data_orcamento_dt"].max().date()
    )

with col3:
    vendedor_sel = st.selectbox(
        "Vendedor",
        options=["Todos"] + sorted(df["vendedor"].dropna().unique().tolist())
    )

# ==========================================================
# FILTRAR ORÇAMENTOS
# ==========================================================

df_orc = df[
    df["status_atual"].isin(["ORCAMENTO", "PEDIDO"])
].copy()

df_orc = df_orc[
    (df_orc["data_orcamento_dt"].dt.date >= data_ini) &
    (df_orc["data_orcamento_dt"].dt.date <= data_fim)
]

if vendedor_sel != "Todos":
    df_orc = df_orc[df_orc["vendedor"] == vendedor_sel]

# ==========================================================
# MÉTRICAS
# ==========================================================

total_orc = len(df_orc)
valor_orc = df_orc["valor_total"].sum()

st.markdown("## Resumo")

m1, m2 = st.columns(2)

with m1:
    st.metric("Quantidade de orçamentos", total_orc)

with m2:
    st.metric(
        "Valor total orçado",
        f"R$ {valor_orc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

# ==========================================================
# ORÇAMENTOS POR VENDEDOR
# ==========================================================

st.markdown("## Orçamentos por vendedor")

orc_vend = (
    df_orc
    .groupby("vendedor")
    .agg(
        quantidade=("chave_orcamento", "count"),
        valor=("valor_total", "sum")
    )
    .reset_index()
    .sort_values("quantidade", ascending=False)
)

st.dataframe(orc_vend, use_container_width=True)

# ==========================================================
# ORÇAMENTOS POR DIA (DATA CORRETA)
# ==========================================================

st.markdown("## Orçamentos por dia")

orc_dia = (
    df_orc
    .dropna(subset=["data_orcamento_dt"])
    .groupby(df_orc["data_orcamento_dt"].dt.date)
    .agg(qtd=("chave_orcamento", "count"))
    .reset_index()
)

st.bar_chart(
    orc_dia.set_index("data_orcamento_dt")["qtd"]
)

# ==========================================================
# TABELA DETALHADA
# ==========================================================

st.markdown("## Detalhamento")

st.dataframe(
    df_orc[
        [
            "chave_orcamento",
            "cliente",
            "vendedor",
            "status_atual",
            "valor_total",
            "data_orcamento_dt",
        ]
    ].sort_values("data_orcamento_dt", ascending=False),
    use_container_width=True
)
