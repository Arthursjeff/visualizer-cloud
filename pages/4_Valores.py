import streamlit as st
import pandas as pd
from utils import carregar_base

st.set_page_config(page_title="Valores", layout="wide")

df = carregar_base()

# =========================
# BASES AUXILIARES
# =========================
df_orcamento = df.copy()
df_aberto = df[df["status_atual"] == "ORCAMENTO"]
df_convertido = df[df["status_atual"].isin(["PEDIDO", "FATURADO"])]

total_qtd = len(df_orcamento)
total_valor = df_orcamento["valor_total"].sum()

aberto_qtd = len(df_aberto)
aberto_valor = df_aberto["valor_total"].sum()

# =========================
# % ORÇAMENTOS EM ABERTO
# =========================
st.subheader("📄 Orçamentos em aberto")

col1, col2 = st.columns(2)

with col1:
    perc_qtd = (aberto_qtd / total_qtd * 100) if total_qtd else 0
    st.metric(
        "% em quantidade",
        f"{perc_qtd:.1f}%"
    )

with col2:
    perc_valor = (aberto_valor / total_valor * 100) if total_valor else 0
    st.metric(
        "% em valor",
        f"{perc_valor:.1f}%"
    )

# =========================
# % CONVERSÃO POR VENDEDOR
# =========================
st.subheader("👤 Conversão por vendedor")

# Total por vendedor
totais_vendedor = (
    df_orcamento
    .groupby("vendedor")
    .size()
    .reset_index(name="total_orcamentos")
)

# Convertidos por vendedor
convertidos_vendedor = (
    df_convertido
    .groupby("vendedor")
    .size()
    .reset_index(name="convertidos")
)

# Merge
conv = (
    totais_vendedor
    .merge(convertidos_vendedor, on="vendedor", how="left")
    .fillna({"convertidos": 0})
)

conv["perc_conversao"] = (
    conv["convertidos"] / conv["total_orcamentos"] * 100
)

conv = conv.sort_values("perc_conversao", ascending=False)

# Exibição em colunas (cards)
cols = st.columns(4)

for i, row in conv.iterrows():
    with cols[i % 4]:
        st.metric(
            row["vendedor"],
            f"{row['perc_conversao']:.1f}%",
            help=f"{int(row['convertidos'])} de {int(row['total_orcamentos'])} orçamentos"
        )
