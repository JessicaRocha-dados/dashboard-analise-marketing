
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Análise de Marketing",
    page_icon="🚀",
    layout="wide"
)

# --- 2. FUNÇÃO DE CARREGAMENTO E PROCESSAMENTO (COM CACHE) ---


@st.cache_data
def carregar_e_processar_dados():
    caminho_do_dataset = 'data/01_raw/marketing_campaign_performance.csv'
    df = pd.read_csv(caminho_do_dataset)

    # Lógica de Limpeza e Engenharia de Atributos
    median_conversions_by_channel = df.groupby(
        'Channel')['Conversions'].transform('median')
    df['Conversions'] = df['Conversions'].fillna(
        median_conversions_by_channel).astype(int)
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    clicks_safe = df['Clicks'].replace(0, 1)
    conversions_safe = df['Conversions'].replace(0, 1)
    budget_safe = df['Budget_BRL'].replace(0, 1)
    df['CTR (%)'] = (df['Clicks'] / df['Impressions']) * 100
    df['CPC'] = df['Budget_BRL'] / clicks_safe
    df['ConversionRate (%)'] = (df['Conversions'] / clicks_safe) * 100
    df['CPA'] = df['Budget_BRL'] / conversions_safe
    AOV = 250
    df['Revenue'] = df['Conversions'] * AOV
    df['ROI (%)'] = ((df['Revenue'] - df['Budget_BRL']) / budget_safe) * 100

    return df


# --- 3. SIDEBAR DE FILTROS ---
st.sidebar.header("Filtros Interativos")
df_original = carregar_e_processar_dados()
canais_selecionados = st.sidebar.multiselect(
    "Canal", options=df_original['Channel'].unique(), default=df_original['Channel'].unique())
regioes_selecionadas = st.sidebar.multiselect(
    "Região", options=df_original['Region'].unique(), default=df_original['Region'].unique())
dispositivos_selecionados = st.sidebar.multiselect(
    "Dispositivo", options=df_original['Device'].unique(), default=df_original['Device'].unique())
df = df_original.query(
    "Channel == @canais_selecionados and Region == @regioes_selecionadas and Device == @dispositivos_selecionados")

# --- 4. LAYOUT DO DASHBOARD PRINCIPAL ---
st.title("🚀 Dashboard de Análise de Marketing")
st.markdown("Esta ferramenta interativa analisa o desempenho das campanhas de marketing para apoiar decisões estratégicas de otimização de orçamento.")
with st.expander("ℹ️ Como usar este dashboard?"):
    st.write("""
        - Use os filtros na barra lateral à esquerda para explorar os dados.
        - Passe o mouse sobre os gráficos para ver detalhes e valores exatos.
        - Os KPIs e gráficos se atualizarão automaticamente com base na sua seleção.
    """)

if df.empty:
    st.warning(
        "Nenhum dado disponível para os filtros selecionados. Por favor, ajuste suas seleções.")
else:
    # KPIs Principais
    st.header("Visão Geral do Período Filtrado")
    col1, col2, col3 = st.columns(3)
    col1.metric("Investimento Total", f"R$ {df['Budget_BRL'].sum():,.2f}")
    col2.metric("Total de Conversões", f"{df['Conversions'].sum():,}")
    col3.metric("ROI Médio", f"{df['ROI (%)'].mean():.2f}%")

    st.markdown("---")

    # --- 5. VISUALIZAÇÕES INTERATIVAS COM PLOTLY ---
    st.header("Análise Detalhada por Canal")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orçamento por Canal")
        budget_by_channel = df.groupby(
            'Channel')['Budget_BRL'].sum().reset_index()
        fig1 = px.pie(budget_by_channel, names='Channel',
                      values='Budget_BRL', hole=.3)
        fig1.update_layout(showlegend=False, height=400,
                           margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Custo por Aquisição (CPA)")
        cpa_by_channel = df.groupby('Channel')['CPA'].mean(
        ).reset_index().sort_values(by='CPA')
        fig2 = px.bar(cpa_by_channel, x='Channel', y='CPA', text_auto='.2f')
        # CORREÇÃO APLICADA AQUI: Usando texttemplate para formatar o texto da barra
        fig2.update_traces(texttemplate='R$ %{y:.2f}', textposition='outside')
        fig2.update_layout(showlegend=False, height=400,
                           margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Conversões por Canal")
        conversions_by_channel = df.groupby('Channel')['Conversions'].sum(
        ).reset_index().sort_values(by='Conversions', ascending=False)
        fig3 = px.bar(conversions_by_channel, x='Channel',
                      y='Conversions', text_auto=True)
        fig3.update_layout(showlegend=False, height=400,
                           margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Retorno (ROI) por Canal")
        roi_by_channel = df.groupby('Channel')['ROI (%)'].mean(
        ).reset_index().sort_values(by='ROI (%)', ascending=False)
        fig4 = px.bar(roi_by_channel, x='Channel',
                      y='ROI (%)', text_auto='.0f')
        # CORREÇÃO APLICADA AQUI: Usando texttemplate para formatar o texto da barra
        fig4.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
        fig4.update_layout(showlegend=False, height=400,
                           margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.header("Explore os Dados Detalhados")
    st.dataframe(df)
