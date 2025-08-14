# page_1.py
# (Código completo e atualizado)

import streamlit as st
from supabase_client import supabase  # Importa o cliente Supabase centralizado
from datetime import datetime
import re

# Função para definir os valores iniciais ou limpar o estado do formulário
def inicializar_estado_formulario():
    """Define ou reseta os valores padrão para cada campo do formulário no session_state."""
    st.session_state.nome = ""
    st.session_state.tipo_pessoa = "Com vínculo"
    st.session_state.vinculo_descricao = ""
    st.session_state.candidato_lideranca = ""
    # Define um município padrão (o primeiro da lista)
    st.session_state.municipio = "Abaetetuba"
    st.session_state.telefone = ""
    # Define um tipo de ajuda padrão
    st.session_state.tipo_ajuda = "Dinheiro"
    st.session_state.descricao_outros = ""
    st.session_state.detalhes = ""
    st.session_state.quantidade = 1
    st.session_state.valor = 0.0

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
    # Garante que o estado do formulário seja inicializado apenas uma vez
    if 'nome' not in st.session_state:
        inicializar_estado_formulario()

    st.title("Formulário de Assistência")

    # --- Seção: Dados Pessoais ---
    with st.expander("Dados Pessoais", expanded=True):
        # Cada widget agora usa uma 'key' para se vincular ao session_state
        nome = st.text_input("Nome *", placeholder="Ex: João da Silva", key="nome")
        tipo_pessoa = st.radio("Tipo de Pessoa *", ["Com vínculo", "Candidato", "Liderança"], key="tipo_pessoa")
        
        # A lógica condicional agora verifica o valor no session_state
        if st.session_state.tipo_pessoa == "Com vínculo":
            vinculo_descricao = st.text_input("Qual Vínculo? *", placeholder="Ex: Indicação do Vereador José", key="vinculo_descricao")
        
        if st.session_state.tipo_pessoa == "Liderança":
            candidato_lideranca = st.text_input("Liderança de qual Candidato? *", placeholder="Ex: Maria Oliveira", key="candidato_lideranca")
            
        st.caption("Preencha os dados pessoais de forma correta para garantir a unicidade do cadastro.")
    
    st.markdown("---")

    # --- Seção: Localização ---
    with st.expander("Localização", expanded=True):
        municipios_para = [
            "Abaetetuba", "Abel Figueiredo", "Acará", "Afuá", "Água Azul do Norte", "Alenquer", 
            "Almeirim", "Altamira", "Anajás", "Ananindeua", "Anapu", "Augusto Corrêa", 
            "Aurora do Pará", "Aveiro", "Bagre", "Baião", "Bannach", "Barcarena", "Belém", 
            "Belterra", "Benevides", "Bom Jesus do Tocantins", "Bonito", "Bragança", "Brasil Novo",
            "Brejo Grande do Araguaia", "Breu Branco", "Breves", "Bujaru", "Cachoeira do Arari", 
            "Cachoeira do Piriá", "Cametá", "Canaã dos Carajás", "Capanema", "Capitão Poço", 
            "Castanhal", "Chaves", "Colares", "Conceição do Araguaia", "Concórdia do Pará", 
            "Cumaru do Norte", "Curionópolis", "Curralinho", "Curuá", "Curuçá", "Dom Eliseu", 
            "Eldorado dos Carajás", "Faro", "Floresta do Araguaia", "Garrafão do Norte", 
            "Goianésia do Pará", "Gurupá", "Igarapé-Açu", "Igarapé-Miri", "Inhangapi", "Ipixuna do Pará", 
            "Irituia", "Itaituba", "Itupiranga", "Jacareacanga", "Jacundá", "Juruti", "Limoeiro do Ajuru",
            "Mãe do Rio", "Magalhães Barata", "Marabá", "Maracanã", "Marapanim", "Marituba", "Medicilândia", 
            "Melgaço", "Mocajuba", "Moju", "Monte Alegre", "Muaná", "Nova Esperança do Piriá", 
            "Nova Ipixuna", "Nova Timboteua", "Novo Progresso", "Novo Repartimento", "Óbidos", 
            "Oeiras do Pará", "Oriximiná", "Ourém", "Ourilândia do Norte", "Pacajá", "Palestina do Pará", 
            "Paragominas", "Parauapebas", "Pau D'Arco", "Peixe-Boi", "Piçarra", "Placas", 
            "Ponta de Pedras", "Portel", "Porto de Moz", "Prainha", "Primavera", "Quatipuru", 
            "Redenção", "Rio Maria", "Rondon do Pará", "Rurópolis", "Salinópolis", "Salvaterra", 
            "Santa Bárbara do Pará", "Santa Cruz do Arari", "Santa Isabel do Pará", "Santa Luzia do Pará", 
            "Santa Maria das Barreiras", "Santa Maria do Pará", "Santana do Araguaia", "Santarém", 
            "Santarém Novo", "Santo Antônio do Tauá", "São Caetano de Odivelas", "São Domingos do Araguaia",
            "São Domingos do Capim", "São Félix do Xingu", "São Francisco do Pará", "São Geraldo do Araguaia", 
            "São João da Ponta", "São João de Pirabas", "São João do Araguaia", "São Miguel do Guamá", 
            "São Sebastião da Boa Vista", "Sapucaia", "Senador José Porfírio", "Soure", "Tailândia", 
            "Terra Alta", "Terra Santa", "Tomé-Açu", "Tracuateua", "Trairão", "Tucumã", "Tucuruí", 
            "Ulianópolis", "Uruará", "Vigia", "Viseu", "Vitória do Xingu", "Xinguara"
        ]
        municipio = st.selectbox("Município *", municipios_para, key="municipio")
        st.caption("Selecione seu município na lista.")
    
    st.markdown("---")

    # --- Seção: Contato ---
    with st.expander("Contato", expanded=True):
        telefone = st.text_input("Telefone *", placeholder="Ex: (91) 98765-4321", key="telefone")
        st.caption("Informe seu telefone, será formatado automaticamente.")
    
    st.markdown("---")

    # --- Seção: Solicitação de Ajuda ---
    with st.expander("Assistência Solicitada", expanded=True):
        tipo_ajuda = st.selectbox("Serviço Requerido *", [
            "Dinheiro", "Cesta Básica", "CredCidadão", "Consulta Médica", "Consulta Odontológica", "Cirurgia Médica", 
            "CredMoradia","Exames Laboratoriais", "Emprego", "Internação Hospitalar", "Transporte/Passagem", "Outros"
        ], key="tipo_ajuda")
        
        if st.session_state.tipo_ajuda == "Outros":
            descricao_outros = st.text_area("Descreva o tipo de ajuda:", placeholder="Detalhe o serviço necessário", key="descricao_outros")
        
        detalhes = st.text_area("Detalhes adicionais:", placeholder="Informe qualquer outra informação relevante", key="detalhes")
        quantidade = st.number_input("Quantidade *", min_value=1, step=1, key="quantidade")
        valor = st.number_input("Valor (R$) *", min_value=0.0, format="%.2f", key="valor")
        st.caption("Preencha as informações sobre a assistência solicitada.")
    
    st.markdown("---")

    if st.button("Enviar", type="primary"):
        # A validação agora usa os valores do st.session_state
        if not st.session_state.nome.strip():
            st.warning("O campo **Nome** é obrigatório! Verifique e tente novamente.")
        elif st.session_state.tipo_pessoa == "Com vínculo" and not st.session_state.vinculo_descricao.strip():
            st.warning("Você selecionou 'Com vínculo'. Por favor, descreva qual é o vínculo.")
        elif st.session_state.tipo_pessoa == "Liderança" and not st.session_state.candidato_lideranca.strip():
            st.warning("Você selecionou 'Liderança'. Informe, por favor, o nome do candidato associado.")
        elif not st.session_state.telefone.strip():
            st.warning("O campo **Telefone** é obrigatório! Certifique-se de preenchê-lo corretamente.")
        elif st.session_state.tipo_ajuda == "Outros" and not st.session_state.descricao_outros.strip():
            st.warning("Para o serviço 'Outros' é necessária uma descrição. Por favor, detalhe o tipo de ajuda.")
        else:
            # Normalização dos dados a partir do session_state
            nome_normalizado = st.session_state.nome.strip().title()
            candidato_normalizado = st.session_state.candidato_lideranca.strip().title()
            vinculo_normalizado = st.session_state.vinculo_descricao.strip()
            telefone_formatado = formatar_telefone(st.session_state.telefone)

            try:
                response = supabase.table('ajuda').select('id').eq('nome', nome_normalizado).eq('telefone', telefone_formatado).execute()
                
                if response.data:
                    st.warning(f"Já existe um registro com o nome **{nome_normalizado}** e o telefone **{telefone_formatado}**.")
                else:
                    # Salva a data no formato ISO 8601, que é o padrão para bancos de dados
                    data_hora = datetime.now().isoformat()
                    
                    dados_para_inserir = {
                        "nome": nome_normalizado,
                        "tipo_pessoa": st.session_state.tipo_pessoa,
                        "vinculo_descricao": vinculo_normalizado, 
                        "candidato_lideranca": candidato_normalizado,
                        "municipio": st.session_state.municipio,
                        "telefone": telefone_formatado,
                        "tipo_ajuda": st.session_state.tipo_ajuda,
                        "descricao_outros": st.session_state.descricao_outros.strip(),
                        "detalhes": st.session_state.detalhes.strip(),
                        "quantidade": st.session_state.quantidade,
                        "valor": st.session_state.valor,
                        "data_hora": data_hora
                    }
                    
                    insert_response = supabase.table('ajuda').insert(dados_para_inserir).execute()

                    if insert_response.data:
                        st.success(f"Registro criado com sucesso!")
                        # Limpa o formulário e força o recarregamento da página
                        inicializar_estado_formulario()
                        st.rerun()
                    else:
                        st.error(f"Ocorreu um erro ao salvar os dados. Detalhes: {insert_response.error.message}")

            except Exception as e:
                st.error(f"Ocorreu um erro na comunicação com o banco de dados.")
                st.error(f"Detalhes do erro: {e}")

app()
