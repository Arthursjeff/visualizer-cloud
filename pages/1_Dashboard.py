# ==========================================================
# DASHBOARD
# ==========================================================

import streamlit as st
import pandas as pd
from utils import carregar_base

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# ==========================================================
# CARREGAR BASE
# ==========================================================

df = carregar_base()

if df.empty:
    st.warning("Base histórica vazia.")
    st.stop()

# Normalizar datas
for col in ["data_orcamento_dt", "data_pedido_dt", "data_faturamento_dt"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# ==========================================================
# DATA DO EVENTO (CHAVE DO DASHBOARD)
# ==========================================================

df["data_evento"] = pd.NaT

df.loc[df["status_atual"] == "ORCAMENTO", "data_evento"] = df.loc[
    df["status_atual"] == "ORCAMENTO", "data_orcamento_dt"
]

df.loc[df["status_atual"] == "PEDIDO", "data_evento"] = df.loc[
    df["status_atual"] == "PEDIDO", "data_pedido_dt"
]

df.loc[df["status_atual"] == "FATURADO", "data_evento"] = df.loc[
    df["status_atual"] == "FATURADO", "data_faturamento_dt"
]

df = df.dropna(subset=["data_evento"]).copy()

# ==========================================================
# FILTRO DE DATA
# ==========================================================

st.markdown("## Filtros")

c1, c2 = st.columns(2)

with c1:
    data_ini = st.date_input(
        "Data inicial",
        value=df["data_evento"].min().date()
    )

with c2:
    data_fim = st.date_input(
        "Data final",
        value=df["data_evento"].max().date()
    )

df_f = df[
    (df["data_evento"].dt.date >= data_ini) &
    (df["data_evento"].dt.date <= data_fim)
].copy()

# ==========================================================
# BASES AUXILIARES
# ==========================================================

df_orc = df_f[df_f["status_atual"] == "ORCAMENTO"]
df_ped = df_f[df_f["status_atual"].isin(["PEDIDO", "FATURADO"])]

# ==========================================================
# MÉTRICAS (3x2)
# ==========================================================

qtd_orc = len(df_orc)
qtd_ped = len(df_ped)

valor_orc = df_orc["valor_total"].sum()
valor_ped = df_ped["valor_total"].sum()

# Conversão
conv_qtd = (qtd_ped / (qtd_orc + qtd_ped)) if (qtd_orc + qtd_ped) > 0 else 0
conv_val = (valor_ped / (valor_orc + valor_ped)) if (valor_orc + valor_ped) > 0 else 0

ticket_medio = (valor_orc / qtd_orc) if qtd_orc > 0 else 0

# Tempo médio de conversão
df_conv = df[
    (df["status_atual"].isin(["PEDIDO", "FATURADO"])) &
    (df["data_orcamento_dt"].notna()) &
    (df["data_pedido_dt"].notna())
].copy()

df_conv["tempo_conv"] = (
    df_conv["data_pedido_dt"] - df_conv["data_orcamento_dt"]
).dt.days

tempo_medio = df_conv["tempo_conv"].mean()

st.markdown("## Resumo")

r1, r2, r3 = st.columns(3)
r4, r5, r6 = st.columns(3)

with r1:
    st.metric("Qtd Orçamentos", qtd_orc)

with r2:
    st.metric("Conversão (Qtd)", f"{conv_qtd*100:.1f}%")

with r3:
    st.metric(
        "Ticket Médio",
        f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

with r4:
    st.metric("Qtd Pedidos (P + F)", qtd_ped)

with r5:
    st.metric("Conversão (Valor)", f"{conv_val*100:.1f}%")

with r6:
    st.metric(
        "Tempo Médio Conversão",
        f"{tempo_medio:.1f} dias" if not pd.isna(tempo_medio) else "-"
    )

# ==========================================================
# EVOLUÇÃO POR DIA
# ==========================================================

st.markdown("## Evolução diária")

dia = (
    df_f
    .groupby(df_f["data_evento"].dt.date)
    .agg(
        orcamentos=("status_atual", lambda x: (x == "ORCAMENTO").sum()),
        pedidos=("status_atual", lambda x: x.isin(["PEDIDO", "FATURADO"]).sum())
    )
    .reset_index()
    .rename(columns={"data_evento": "data"})
)

st.bar_chart(
    dia.set_index("data")
)
