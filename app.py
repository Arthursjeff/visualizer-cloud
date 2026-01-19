import streamlit as st
from utils import carregar_base

st.set_page_config(
    page_title="Análise Comercial",
    layout="wide"
)

st.title("📊 Análise Comercial – Jefferson")

st.markdown(
    """
    Bem-vindo ao painel de análise.

    Use o menu à esquerda para navegar entre:
    - Dashboard resumido
    - Orçamentos
    - Vendas
    - Valores
    """
)

# teste de leitura da base
try:
    df = carregar_base()
    st.success(f"Base carregada com {df.shape[0]} registros.")
except Exception as e:
    st.error(str(e))
