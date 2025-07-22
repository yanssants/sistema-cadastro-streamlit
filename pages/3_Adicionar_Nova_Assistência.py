# page_3.py
# (Código completo e atualizado para usar Supabase)

import streamlit as st
from supabase_client import supabase  # Importa o cliente Supabase centralizado
from datetime import datetime

def app():
    st.title("➕ Adicionar Nova Assistência")

    # Inicializa o session_state para manter os dados da pessoa encontrada
    if 'pessoa_encontrada' not in st.session_state:
        st.session_state.pessoa_encontrada = False
        st.session_state.pessoa_info = None

    # --- Seção: Busca de Registro ---
    with st.expander("🔍 Buscar Registro para Adicionar Ajuda", expanded=not st.session_state.pessoa_encontrada):
        with st.form(key="form_buscar_pessoa"):
            nome_busca = st.text_input("Digite o nome para buscar o registro", placeholder="Ex: João da Silva")
            buscar_btn = st.form_submit_button("Buscar Registro")

        if buscar_btn:
            if not nome_busca.strip():
                st.warning("Por favor, digite um nome para buscar.")
                st.session_state.pessoa_encontrada = False
                st.session_state.pessoa_info = None
            else:
                try:
                    # Realiza a busca por nome (case-insensitive) e pega o primeiro resultado
                    response = supabase.table('ajuda') \
                        .select('id, nome, tipo_pessoa, municipio') \
                        .ilike('nome', f'%{nome_busca.strip()}%') \
                        .limit(1).single().execute()
                    
                    resultado = response.data
                    
                    if not resultado:
                        st.error("Nenhum registro encontrado para este nome.")
                        st.session_state.pessoa_encontrada = False
                        st.session_state.pessoa_info = None
                    else:
                        st.session_state.pessoa_info = resultado
                        st.session_state.pessoa_encontrada = True
                        st.success(f"Registro encontrado: **{resultado['nome']}**")
                        # Força o rerender para fechar este expander e abrir os outros
                        st.rerun()

                except Exception as e:
                    st.error("Nenhum registro encontrado ou ocorreu um erro durante a busca.")
                    st.info("Dica: Se houver múltiplos nomes parecidos, a busca pode falhar. Tente ser mais específico.")
                    st.session_state.pessoa_encontrada = False
                    st.session_state.pessoa_info = None
    
    # Se uma pessoa foi encontrada, mostra as seções para adicionar a ajuda
    if st.session_state.pessoa_encontrada:
        pessoa = st.session_state.pessoa_info

        # --- Seção: Resumo do Registro Encontrado ---
        with st.expander("📄 Resumo do Registro Encontrado", expanded=True):
            st.markdown(f"""
            - **Nome:** `{pessoa['nome']}`
            - **Tipo de Pessoa:** `{pessoa['tipo_pessoa']}`
            - **Município:** `{pessoa['municipio']}`
            - **ID do Registro:** `{pessoa['id']}`
            """)

        st.markdown("---")

        # --- Seção: Formulário para Nova Ajuda ---
        with st.expander("📝 Adicionar Nova Ajuda", expanded=True):
            tipo_ajuda = st.selectbox("Tipo de Ajuda *", [
                "Dinheiro", "Cesta Básica", "CredCidadão", "Consulta Médica", "Consulta Odontológica", 
                "Exames Laboratoriais", "Emprego", "Internação Hospitalar", "Transporte/Passagem", "Outros"
            ], key="tipo_ajuda_extra")
            
            if tipo_ajuda == "Outros":
                descricao_outros = st.text_area("Descreva o tipo de ajuda:", placeholder="Forneça detalhes sobre o serviço requerido")
            else:
                descricao_outros = ""

            quantidade = st.number_input("Quantidade *", min_value=1, value=1, step=1, key="qtd_extra")
            valor = st.number_input("Valor (R$) *", min_value=0.0, format="%.2f", value=0.0, key="valor_extra")
            detalhes = st.text_area("Detalhes (opcional)", placeholder="Adicione mais informações se necessário", key="detalhes_extra")

            if st.button("Salvar Nova Ajuda", type="primary"):
                if tipo_ajuda == "Outros" and not descricao_outros.strip():
                    st.error("Para o serviço 'Outros', a descrição é obrigatória.")
                else:
                    try:
                        data_hora = datetime.now().strftime("%d/%m/%Y - %H:%M")
                        
                        dados_nova_ajuda = {
                            "ajuda_id": pessoa['id'],
                            "tipo_ajuda": tipo_ajuda.strip(),
                            "descricao_outros": descricao_outros.strip(),
                            "detalhes": detalhes.strip(),
                            "quantidade": quantidade,
                            "valor": valor,
                            "data_hora": data_hora
                        }
                        
                        insert_response = supabase.table('ajuda_extra').insert(dados_nova_ajuda).execute()

                        if insert_response.data:
                            st.success(f"Nova ajuda adicionada com sucesso para **{pessoa['nome']}** em {data_hora}.")
                            # Limpa o estado para permitir uma nova busca
                            st.session_state.pessoa_encontrada = False
                            st.session_state.pessoa_info = None
                            # Limpa os campos do formulário forçando um rerun
                            st.rerun()
                        else:
                            st.error(f"Ocorreu um erro ao salvar a nova ajuda. Detalhes: {insert_response.error.message}")

                    except Exception as e:
                        st.error(f"Ocorreu um erro crítico ao salvar os dados. Detalhes: {e}")
        
        # Botão para cancelar e buscar outra pessoa
        if st.button("Cancelar e Buscar Outra Pessoa"):
            st.session_state.pessoa_encontrada = False
            st.session_state.pessoa_info = None
            st.rerun()
            
app()