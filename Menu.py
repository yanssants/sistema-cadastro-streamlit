# main.py (Versão final e simplificada)

import streamlit as st

# Configuração da página (pode ser a primeira coisa no seu script)
st.set_page_config(
    page_title="Sistema de Gestão",
    page_icon="🤝",
    layout="wide"
)

# Conteúdo da Página Principal (Home)
st.title("Bem-vindo ao Sistema de Gestão de Assistência")
st.sidebar.success("Selecione uma página no menu ao lado.")

st.markdown("---")
st.markdown(
    """
    Este é o sistema para gerenciar registros de assistência.
    
    ### Funcionalidades
    
    Use o menu na barra lateral à esquerda para navegar entre as seções:
    
    - **Cadastro:** Para criar novos registros de assistência.
    - **Consulta:** Para buscar, filtrar e visualizar registros existentes.
    - **Adicionar Nova Ajuda:** Para incluir novas assistências a uma pessoa já cadastrada.
    - **Editar:** Para modificar ou excluir registros existentes.
    - **Dashboard:** Para ter uma visão geral e gráfica dos dados.
    
    Selecione a opção desejada para começar!
    """
)

# Você não precisa mais do selectbox ou do bloco if/elif aqui.
# O Streamlit gera o menu automaticamente a partir da pasta 'pages'.

#---------------------------------------------------------------------------------------

#streamlit run Menu.py