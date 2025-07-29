# page_2.py
# (Código atualizado para exibir o campo "vinculo_descricao")

import streamlit as st
from supabase_client import supabase # Importa o cliente Supabase centralizado

def app():
    st.title("📋 Consulta de Registros")

    # Campo de busca por nome
    nome_busca = st.text_input("🔍 Buscar por nome", placeholder="Digite o nome completo ou parte dele")
    
    # Lista de municípios (igual à utilizada na page 1)
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
    
    # Filtros avançados
    with st.expander("Filtros Avançados", expanded=False):
        municipio_filtro = st.selectbox("Filtrar por Município", ["Todos"] + municipios_para)
        # 1. ALTERADO: "Sem vínculo" para "Com vínculo"
        tipo_pessoa_filtro = st.selectbox("Filtrar por Tipo de Pessoa", ["Todos", "Com vínculo", "Candidato", "Liderança"])
        tipo_ajuda_filtro = st.selectbox("Filtrar por Tipo de Ajuda (Principal)", ["Todos", "Dinheiro", "Cesta Básica", "CredCidadão", "Atendimento Médica", "Exames", "Emprego", "Internação Hospitalar", "Transporte/Passagem", "Outros"])

    st.markdown("---")

    # Botão para realizar a busca com a nova lógica do Supabase
    if st.button("Buscar", type="primary"):
        try:
            # Constrói a query no Supabase de forma encadeada
            # 'select("*, ajuda_extra(*)")' faz o "JOIN" automaticamente
            query = supabase.table('ajuda').select('*, ajuda_extra(*)').order('nome', desc=False)

            # Aplica os filtros se eles foram selecionados
            if nome_busca.strip():
                query = query.ilike('nome', f'%{nome_busca.strip()}%')
            
            if municipio_filtro != "Todos":
                query = query.eq('municipio', municipio_filtro)
            
            if tipo_pessoa_filtro != "Todos":
                query = query.eq('tipo_pessoa', tipo_pessoa_filtro)
            
            if tipo_ajuda_filtro != "Todos":
                query = query.eq('tipo_ajuda', tipo_ajuda_filtro)
            
            # Executa a query
            response = query.execute()
            resultados = response.data

            if not resultados:
                st.error("Nenhum registro encontrado para os critérios informados. Verifique os filtros e tente novamente.")
            else:
                st.success(f"{len(resultados)} registro(s) encontrado(s).")
                st.markdown("---")

                # Exibe os resultados
                for dados in resultados:
                    with st.container(border=True):
                        st.markdown(f"### {dados.get('nome', 'Nome não informado')}")
                        st.write(f"**Cadastro realizado em:** {dados.get('data_hora', 'N/A')}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Tipo de Pessoa:** {dados.get('tipo_pessoa', 'N/A')}")
                            # 2. ADICIONADO: Exibe a descrição do vínculo se houver
                            if dados.get('tipo_pessoa') == "Com vínculo":
                                st.write(f"**Vínculo:** {dados.get('vinculo_descricao', 'N/A')}")
                            if dados.get('tipo_pessoa') == "Liderança":
                                st.write(f"**Candidato:** {dados.get('candidato_lideranca', 'N/A')}")
                        with col2:
                            st.write(f"**Município:** {dados.get('municipio', 'N/A')}")
                        with col3:
                            st.write(f"**Telefone:** {dados.get('telefone', 'N/A')}")
                        
                        st.markdown("---")
                        st.markdown("**Assistência Principal:**", help="Registro inicial feito no formulário.")
                        
                        valor_principal = float(dados.get('valor', 0.0))
                        valor_formatado_principal = f"R$ {valor_principal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        
                        st.write(f"- **Tipo:** {dados.get('tipo_ajuda', 'N/A')}")
                        if dados.get('descricao_outros'):
                            st.write(f"- **Descrição:** {dados.get('descricao_outros')}")
                        st.write(f"- **Quantidade:** {dados.get('quantidade', 0)}")
                        st.write(f"- **Valor:** {valor_formatado_principal}")
                        
                        if dados.get('detalhes'):
                            st.markdown("**Detalhes Adicionais:**")
                            st.info(f"{dados.get('detalhes')}")
                        
                        ajudas_extras = dados.get('ajuda_extra', [])
                        if ajudas_extras:
                            with st.expander(f"Ajudas Extras ({len(ajudas_extras)})", expanded=False):
                                for ajuda in ajudas_extras:
                                    st.markdown("---")
                                    valor_extra = float(ajuda.get('valor', 0.0))
                                    valor_formatado_extra = f"R$ {valor_extra:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                                    
                                    st.write(f"**Tipo de Ajuda:** {ajuda.get('tipo_ajuda', 'N/A')}")
                                    if ajuda.get('descricao_outros'):
                                        st.write(f"**Descrição:** {ajuda.get('descricao_outros')}")
                                    st.write(f"**Quantidade:** {ajuda.get('quantidade', 0)}")
                                    st.write(f"**Valor:** {valor_formatado_extra}")
                                    st.write(f"**Adicionado em:** {ajuda.get('data_hora', 'N/A')}")
                        else:
                            st.info("Nenhuma ajuda extra registrada para esta pessoa.")
                    st.markdown("---")

        except Exception as e:
            st.error("Ocorreu um erro ao buscar os registros no banco de dados.")
            st.error(f"Detalhes do erro: {e}")

app()
