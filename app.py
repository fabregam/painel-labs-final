import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ficar larga e bonita
st.set_page_config(page_title="Gestão de Laboratórios - TO", layout="wide")

# Título e Estilo
st.markdown("# 📊 Painel de Gestão: Laboratórios de Ciências")
st.markdown("---")

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_excel("Base_Consolidada_Laboratorios.xlsx")
    df.columns = df.columns.astype(str).str.strip()
    if 'LAB' in df.columns:
        df['LAB'] = pd.to_numeric(df['LAB'], errors='coerce').fillna(0)
    return df

try:
    df = load_data()

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("Filtros de Navegação")
    sre_lista = ["TODAS"] + sorted(df['SRE'].unique().tolist())
    sre_sel = st.sidebar.selectbox("Selecione a Regional (SRE):", sre_lista)

    # Filtragem dos dados
    if sre_sel == "TODAS":
        df_filt = df
    else:
        df_filt = df[df['SRE'] == sre_sel]

    # --- METRICAS PRINCIPAIS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Escolas", len(df_filt))
    with col2:
        st.metric("Total de Laboratórios", int(df_filt['LAB'].sum()))
    with col3:
        st.metric("Municípios Atendidos", len(df_filt['MUNICIPIO'].unique()))

    st.markdown("---")

    # --- GRÁFICO INTERATIVO ---
    st.subheader(f"Distribuição por Município - {sre_sel}")
    resumo_mun = df_filt.groupby("MUNICIPIO")["LAB"].sum().reset_index()
    resumo_mun = resumo_mun[resumo_mun['LAB'] > 0].sort_values("LAB", ascending=False)

    if not resumo_mun.empty:
        fig = px.bar(resumo_mun, 
                     x="MUNICIPIO", 
                     y="LAB", 
                     text="LAB",
                     color="LAB",
                     color_continuous_scale="Blues",
                     labels={'LAB': 'Qtd Labs', 'MUNICIPIO': 'Cidade'})
        
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum laboratório registado para esta seleção.")

    # --- TABELA DE DADOS ---
    with st.expander("Ver Lista Detalhada de Escolas"):
        st.dataframe(df_filt[["MUNICIPIO", "ESCOLA", "TIPO_ESCOLA", "LAB"]].sort_values("MUNICIPIO"), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o ficheiro: {e}")
    st.info("Certifique-se de que o ficheiro 'Base_Consolidada_Laboratorios.xlsx' está na mesma pasta que este app.")
