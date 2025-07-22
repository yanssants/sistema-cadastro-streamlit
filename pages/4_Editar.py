# page_4.py
# (Código completo e atualizado para usar Supabase)

import streamlit as st
from supabase_client import supabase # Importa o cliente Supabase centralizado
import re

def formatar_telefone(telefone):
    """
    Remove caracteres não numéricos e formata o telefone para o padrão (XX) XXXXX-XXXX.
    """
    if not isinstance(telefone, str):
        return ""
    digits = re.sub(r'\D', '', telefone)
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    else:
        return telefone

def app():
    st.title("📝 Editar Registro e Ajudas Extras")

    # Inicializa o estado da sessão
    if 'registros_encontrados' not in st.session_state:
        st.session_state.registros_encontrados = []
    if 'id_registro_selecionado' not in st.session_state:
        st.session_state.id_registro_selecionado = None

    # --- Formulário de busca ---
    with st.form(key="form_buscar"):
        nome_busca = st.text_input("🔍 Buscar por nome", 
                                   placeholder="Digite o nome ou deixe em branco para listar todos")
        buscar = st.form_submit_button("Buscar Registros")
    
    if buscar:
        try:
            # Usa o Supabase para buscar os registros
            query = supabase.table('ajuda').select('id, nome').order('nome')
            if nome_busca.strip():
                query = query.ilike('nome', f'%{nome_busca.strip()}%')
            
            response = query.execute()
            st.session_state.registros_encontrados = response.data
            st.session_state.id_registro_selecionado = None # Reseta a seleção anterior
            if not response.data:
                st.info("Nenhum registro encontrado com este nome.")

        except Exception as e:
            st.error(f"Erro ao buscar registros: {e}")
            st.session_state.registros_encontrados = []

    # Se encontrou registros, mostra a caixa de seleção
    if st.session_state.registros_encontrados:
        # Cria as opções para o selectbox no formato "Nome (ID: X)"
        opcoes = {f"{reg['nome']} (ID: {reg['id']})": reg['id'] 
                  for reg in st.session_state.registros_encontrados}
        
        selecionado_label = st.selectbox("Selecione o registro para editar", list(opcoes.keys()))
        
        if selecionado_label:
            st.session_state.id_registro_selecionado = opcoes[selecionado_label]

    # Se um registro foi selecionado, carrega e exibe os formulários de edição
    if st.session_state.id_registro_selecionado:
        idr = st.session_state.id_registro_selecionado

        try:
            # Carrega dados do registro principal e suas ajudas extras com uma única chamada
            response = supabase.table('ajuda').select('*, ajuda_extra(*)').eq('id', idr).single().execute()
            reg = response.data
            
            if not reg:
                st.error("Não foi possível carregar os dados do registro selecionado.")
                return

        except Exception as e:
            st.error(f"Erro ao carregar dados detalhados do registro: {e}")
            return

        st.markdown("---")
        st.subheader(f"Editando: {reg.get('nome', '')}")

        # --- Formulário para editar registro principal ---
        with st.form(key="form_editar_principal"):
            st.markdown("**Dados do Registro Principal**")
            
            novo_nome = st.text_input("Nome *", value=reg.get('nome', ''))
            tipos_pessoa_map = ["Sem vínculo", "Candidato", "Liderança"]
            novo_tipo_pessoa = st.radio(
                "Tipo de Pessoa *",
                tipos_pessoa_map,
                index=tipos_pessoa_map.index(reg.get('tipo_pessoa')) if reg.get('tipo_pessoa') in tipos_pessoa_map else 0
            )
            novo_cand = st.text_input("Candidato associado *", value=reg.get('candidato_lideranca', '')) if novo_tipo_pessoa == "Liderança" else ""
            
            municipios_para = ["Abaetetuba", "Abel Figueiredo", "Acará", "etc..."] # Use sua lista completa aqui
            novo_mun = st.selectbox("Município *", municipios_para, index=municipios_para.index(reg.get('municipio')) if reg.get('municipio') in municipios_para else 0)
            
            novo_tel = st.text_input("Telefone *", value=reg.get('telefone', ''))
            
            servicos = ["Dinheiro", "Cesta Básica", "CredCidadão", "Consulta Médica", "Consulta Odontológica", "Exames Laboratoriais", "Emprego", "Internação Hospitalar", "Transporte/Passagem", "Outros"]
            novo_tipo_ajuda = st.selectbox("Serviço Requerido *", servicos, index=servicos.index(reg.get('tipo_ajuda')) if reg.get('tipo_ajuda') in servicos else 0)
            
            novo_desc = st.text_area("Descreva o serviço:", value=reg.get('descricao_outros', '')) if novo_tipo_ajuda == "Outros" else ""
            
            novo_qtd = st.number_input("Quantidade *", min_value=1, value=reg.get('quantidade', 1), step=1)
            novo_val = st.number_input("Valor (R$)*", min_value=0.0, format="%.2f", value=float(reg.get('valor', 0.0)))
            novo_det = st.text_area("Detalhes adicionais (opcional)", value=reg.get('detalhes', ''))

            alterar_principal = st.form_submit_button("✅ Salvar Alterações do Registro Principal", type="primary")

        if alterar_principal:
            if novo_tipo_pessoa == "Liderança" and not novo_cand.strip():
                st.error("Para 'Liderança', o nome do candidato associado é obrigatório.")
            else:
                try:
                    update_data = {
                        "nome": novo_nome.strip().title(),
                        "tipo_pessoa": novo_tipo_pessoa,
                        "candidato_lideranca": novo_cand.strip().title(),
                        "municipio": novo_mun,
                        "telefone": formatar_telefone(novo_tel),
                        "tipo_ajuda": novo_tipo_ajuda,
                        "descricao_outros": novo_desc.strip(),
                        "quantidade": novo_qtd,
                        "valor": novo_val,
                        "detalhes": novo_det.strip()
                    }
                    supabase.table('ajuda').update(update_data).eq('id', idr).execute()
                    st.success("Registro principal atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar o registro principal: {e}")

        # --- Edição de Ajudas Extras ---
        st.markdown("---")
        st.subheader("📌 Edição de Ajudas Extras")

        extras = reg.get('ajuda_extra', [])
        if not extras:
            st.info("Não há ajudas extras para este registro.")
        else:
            for ext in extras:
                ext_id = ext['id']
                with st.expander(f"Ajuda Extra #{ext_id} — cadastrada em {ext.get('data_hora', 'N/A')}"):
                    with st.form(key=f"form_extra_{ext_id}"):
                        novo_tipo_ext = st.selectbox("Tipo de Ajuda", servicos, index=servicos.index(ext.get('tipo_ajuda')) if ext.get('tipo_ajuda') in servicos else 0, key=f"tipo_{ext_id}")
                        novo_desc_ext = st.text_area("Descreva o serviço:", value=ext.get('descricao_outros', ''), key=f"desc_{ext_id}") if novo_tipo_ext == "Outros" else ""
                        novo_qtd_ext = st.number_input("Quantidade", min_value=1, value=ext.get('quantidade', 1), step=1, key=f"qtd_{ext_id}")
                        novo_val_ext = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", value=float(ext.get('valor', 0.0)), key=f"val_{ext_id}")
                        novo_det_ext = st.text_area("Detalhes adicionais", value=ext.get('detalhes', ''), key=f"det_{ext_id}")

                        col1, col2 = st.columns([3, 1])
                        with col1:
                            alterar_extra = st.form_submit_button("✅ Salvar Alterações da Ajuda Extra")
                        with col2:
                            excluir_extra = st.form_submit_button("❌ Excluir Ajuda Extra")

                    if alterar_extra:
                        try:
                            update_data_ext = {
                                "tipo_ajuda": novo_tipo_ext,
                                "descricao_outros": novo_desc_ext.strip(),
                                "quantidade": novo_qtd_ext,
                                "valor": novo_val_ext,
                                "detalhes": novo_det_ext.strip()
                            }
                            supabase.table('ajuda_extra').update(update_data_ext).eq('id', ext_id).execute()
                            st.success(f"A ajuda extra #{ext_id} foi atualizada com sucesso! A página será recarregada.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar a ajuda extra #{ext_id}: {e}")

                    if excluir_extra:
                        try:
                            supabase.table('ajuda_extra').delete().eq('id', ext_id).execute()
                            st.success(f"A ajuda extra #{ext_id} foi excluída com sucesso! A página será recarregada.")
                            st.rerun() # Recarrega a página para refletir a exclusão
                        except Exception as e:
                            st.error(f"Erro ao excluir a ajuda extra #{ext_id}: {e}")

app()