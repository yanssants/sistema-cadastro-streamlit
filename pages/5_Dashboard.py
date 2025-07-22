# page_5.py
# (Código completo e atualizado para usar Supabase)

import streamlit as st
import pandas as pd
from supabase_client import supabase  # Importa o cliente Supabase centralizado
from streamlit_echarts import st_echarts

def app():
    st.title("📊 Dashboard de Registros")

    try:
        # --- Carrega dados do Supabase ---
        response_main = supabase.table('ajuda').select('*').execute()
        response_extra = supabase.table('ajuda_extra').select('*').execute()

        df_main = pd.DataFrame(response_main.data)
        df_extra = pd.DataFrame(response_extra.data)

    except Exception as e:
        st.error("Falha ao carregar dados do Supabase. Verifique a conexão e as credenciais.")
        st.error(f"Detalhes: {e}")
        return

    if df_main.empty:
        st.warning("Ainda não há registros na base de dados para exibir no dashboard.")
        return

    # --- Prepara os dados (lógica original mantida) ---
    df_main['data_hora'] = pd.to_datetime(df_main['data_hora'],
                                          format="%d/%m/%Y - %H:%M",
                                          errors='coerce')
    df_main.dropna(subset=['data_hora'], inplace=True)

    # Renomeia colunas de ajuda_extra para evitar conflitos no merge
    df_extra.rename(columns={
        'tipo_ajuda': 'tipo_ajuda_extra',
        'quantidade': 'quantidade_extra',
        'valor': 'valor_extra'
    }, inplace=True)

    # Junta df_extra com colunas de df_main para permitir filtros cruzados
    df_merged_extra = pd.merge(
        df_extra,
        df_main[['id', 'data_hora', 'tipo_pessoa', 'municipio']],
        left_on='ajuda_id', right_on='id', how='left'
    )

    # --- Sidebar de filtros ---
    st.sidebar.header("🔎 Filtros do Dashboard")
    
    # Prepara os valores padrão para os filtros
    dmin_safe = df_main['data_hora'].dt.date.min() if not df_main.empty else pd.Timestamp.now().date()
    dmax_safe = df_main['data_hora'].dt.date.max() if not df_main.empty else pd.Timestamp.now().date()
    
    start_date, end_date = st.sidebar.date_input("Período de Análise", [dmin_safe, dmax_safe])
    
    # Filtros de multiselect
    tipos_pessoa_opcoes = df_main['tipo_pessoa'].unique()
    tipos_pessoa = st.sidebar.multiselect("Tipo de Pessoa",
                                          options=tipos_pessoa_opcoes,
                                          default=tipos_pessoa_opcoes)

    municipios_opcoes = sorted(df_main['municipio'].unique())
    municipios_selecionados = st.sidebar.multiselect("Municípios",
                                                     options=municipios_opcoes,
                                                     default=municipios_opcoes)
    
    # Combina tipos de ajuda principal e extra para um filtro unificado
    tipos_ajuda_opcoes = pd.concat([df_main['tipo_ajuda'], df_merged_extra['tipo_ajuda_extra']]).unique()
    tipos_ajuda_selecionados = st.sidebar.multiselect("Tipos de Assistência",
                                                      options=tipos_ajuda_opcoes,
                                                      default=tipos_ajuda_opcoes)

    # --- Aplica filtros aos DataFrames ---
    mask_main = (
        (df_main['data_hora'].dt.date >= start_date) &
        (df_main['data_hora'].dt.date <= end_date) &
        (df_main['tipo_pessoa'].isin(tipos_pessoa)) &
        (df_main['municipio'].isin(municipios_selecionados)) &
        (df_main['tipo_ajuda'].isin(tipos_ajuda_selecionados))
    )
    dfm = df_main.loc[mask_main]

    mask_extra = (
        (df_merged_extra['data_hora'].dt.date >= start_date) &
        (df_merged_extra['data_hora'].dt.date <= end_date) &
        (df_merged_extra['tipo_pessoa'].isin(tipos_pessoa)) &
        (df_merged_extra['municipio'].isin(municipios_selecionados)) &
        (df_merged_extra['tipo_ajuda_extra'].isin(tipos_ajuda_selecionados))
    )
    dfe = df_merged_extra.loc[mask_extra]

    # --- Exibição dos Gráficos e Métricas ---
    
    # Indicadores
    total_pessoas_atendidas = dfm['id'].nunique()
    total_assistencias = int(dfm['quantidade'].sum() + dfe['quantidade_extra'].sum())

    st.markdown("### 📌 Indicadores Gerais")
    col1, col2 = st.columns(2)
    col1.metric("Total de Pessoas Atendidas", f"{total_pessoas_atendidas:,}".replace(",", "."))
    col2.metric("Total de Assistências Prestadas", f"{total_assistencias:,}".replace(",", "."))
    st.markdown("---")

    # Gráfico: Distribuição por Tipo de Ajuda
    st.markdown("### 📦 Distribuição por Tipo de Assistência")
    dist_main = dfm.groupby('tipo_ajuda')['quantidade'].sum()
    dist_extra = dfe.groupby('tipo_ajuda_extra')['quantidade_extra'].sum()
    dist_total = dist_main.add(dist_extra, fill_value=0).sort_values(ascending=False)

    if not dist_total.empty:
        option_pie = {
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
            "legend": {"orient": "vertical", "left": "left"},
            "series": [{
                "name": "Tipo de Assistência",
                "type": "pie",
                "radius": "70%",
                "data": [{"value": int(v), "name": k} for k, v in dist_total.items()],
                "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}}
            }]
        }
        st_echarts(option_pie, height="500px")
    else:
        st.info("Sem dados de assistência para o período e filtros selecionados.")
    
    st.markdown("---")

    # Gráfico: Registros por Município
    st.markdown("### 🗺️ Pessoas Atendidas por Município")
    mun_counts = dfm['municipio'].value_counts().sort_values(ascending=False)
    
    if not mun_counts.empty:
        option_bar_mun = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": '3%', "right": '4%', "bottom": '3%', "containLabel": True},
            "xAxis": {"type": 'value', "boundaryGap": [0, 0.01]},
            "yAxis": {"type": 'category', "data": list(mun_counts.index)[::-1]}, # Invertido para mostrar o maior em cima
            "series": [{
                "name": 'Pessoas Atendidas',
                "type": 'bar',
                "data": [int(v) for v in mun_counts.values][::-1] # Invertido
            }]
        }
        st_echarts(option_bar_mun, height=f"{max(400, len(mun_counts) * 35)}px")
    else:
        st.info("Sem dados de municípios para o período e filtros selecionados.")

app()