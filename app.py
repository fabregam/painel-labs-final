import streamlit as st
import pandas as pd
import sys

# Configuração da página
st.set_page_config(page_title="Painel Laboratórios", layout="wide")

st.title("📊 Painel de Controle de Laboratórios")

# Mostra a versão para sabermos se o erro do Python 3.14 foi corrigido
st.sidebar.info(f"Versão do Python: {sys.version[:6]}")

try:
    # Tenta ler o seu arquivo Excel
    nome_arquivo = "Base_Consolidada_Laboratorios.xlsx"
    df = pd.read_excel(nome_arquivo)
    
    st.success(f"✅ Arquivo '{nome_arquivo}' carregado com sucesso!")
    
    # Exibe uma amostra dos dados
    st.subheader("Dados do Laboratório")
    st.dataframe(df)

except Exception as e:
    st.error(f"❌ Erro ao carregar os dados: {e}")
    st.warning("Verifique se o nome do arquivo Excel no GitHub é exatamente: Base_Consolidada_Laboratorios.xlsx")
