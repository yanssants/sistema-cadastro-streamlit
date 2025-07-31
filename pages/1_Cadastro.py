# page_1.py
# (Código completo e atualizado para usar Supabase com a nova lógica de "Com Vínculo" e Fuso Horário)

import streamlit as st
from supabase_client import supabase  # Importa o cliente Supabase centralizado
from datetime import datetime
import re  # Usado para limpar o telefone
import pytz # ADICIONADO: Para manipulação de fusos horários

def formatar_telefone(telefone):
    """
    Remove caracteres não numéricos e formata o telefone para o padrão (XX) XXXXX-XXXX.
    Caso o número não possua 11 dígitos, retorna o telefone sem formatação.
    """
    if not isinstance(telefone, str):
        return ""
    digits = re.sub(r'\D', '', telefone)
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    else:
        return telefone

def app():
    # A conexão com o banco e a criação de tabelas são removidas daqui
    # pois agora são gerenciadas pelo Supabase.

    st.title("Formulário de Assistência")

    # --- Seção: Dados Pessoais ---
    with st.expander("Dados Pessoais", expanded=True):
        nome = st.text_input("Nome *", placeholder="Ex: João da Silva")
        # Alterado de "Sem vínculo" para "Com vínculo"
        tipo_pessoa = st.radio("Tipo de Pessoa *", ["Com vínculo", "Candidato", "Liderança"])
        
        # Campo condicional para "Com vínculo"
        if tipo_pessoa == "Com vínculo":
            vinculo_descricao = st.text_input("Qual Vínculo? *", placeholder="Ex: Indicação do Vereador José")
        else:
            vinculo_descricao = ""
            
        # Campo condicional para "Liderança"
        if tipo_pessoa == "Liderança":
            candidato_lideranca = st.text_input("Liderança de qual Candidato? *", placeholder="Ex: Maria Oliveira")
        else:
            candidato_lideranca = ""
            
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
        municipio = st.selectbox("Município *", municipios_para)
        st.caption("Selecione seu município na lista.")
    
    st.markdown("---")

    # --- Seção: Contato ---
    with st.expander("Contato", expanded=True):
        telefone = st.text_input("Telefone *", placeholder="Ex: (91) 98765-4321")
        st.caption("Informe seu telefone, será formatado automaticamente.")
    
    st.markdown("---")

    # --- Seção: Solicitação de Ajuda ---
    with st.expander("Assistência Solicitada", expanded=True):
        tipo_ajuda = st.selectbox("Serviço Requerido *", [
            "Dinheiro", "Cesta Básica", "CredCidadão", "Consulta Médica", "Consulta Odontológica", "Cirurgia Médica", 
            "CredMoradia","Exames Laboratoriais", "Emprego", "Internação Hospitalar", "Transporte/Passagem", "Outros"
        ])
        if tipo_ajuda == "Outros":
            descricao_outros = st.text_area("Descreva o tipo de ajuda:", placeholder="Detalhe o serviço necessário")
        else:
            descricao_outros = ""
        
        detalhes = st.text_area("Detalhes adicionais:", placeholder="Informe qualquer outra informação relevante")
        quantidade = st.number_input("Quantidade *", min_value=1, value=1, step=1)
        valor = st.number_input("Valor (R$) *", min_value=0.0, format="%.2f")
        st.caption("Preencha as informações sobre a assistência solicitada.")
    
    st.markdown("---")

    # Botão de envio com a nova lógica do Supabase
    if st.button("Enviar", type="primary"):
        # Validação dos campos obrigatórios
        if not nome.strip():
            st.warning("O campo **Nome** é obrigatório! Verifique e tente novamente.")
        # Nova validação para "Com vínculo"
        elif tipo_pessoa == "Com vínculo" and not vinculo_descricao.strip():
            st.warning("Você selecionou 'Com vínculo'. Por favor, descreva qual é o vínculo.")
        elif tipo_pessoa == "Liderança" and not candidato_lideranca.strip():
            st.warning("Você selecionou 'Liderança'. Informe, por favor, o nome do candidato associado.")
        elif not telefone.strip():
            st.warning("O campo **Telefone** é obrigatório! Certifique-se de preenchê-lo corretamente.")
        elif tipo_ajuda == "Outros" and not descricao_outros.strip():
            st.warning("Para o serviço 'Outros' é necessária uma descrição. Por favor, detalhe o tipo de ajuda.")
        else:
            # Normalização dos dados
            nome_normalizado = nome.strip().title()
            candidato_normalizado = candidato_lideranca.strip().title() if candidato_lideranca else ""
            # Adicionada a normalização do novo campo
            vinculo_normalizado = vinculo_descricao.strip() if vinculo_descricao else ""
            municipio_normalizado = municipio.strip().title()
            telefone_formatado = formatar_telefone(telefone)
            tipo_ajuda_normalizado = tipo_ajuda.strip()
            descricao_normalizada = descricao_outros.strip()
            detalhes_normalizados = detalhes.strip()

            try:
                # Verificação de duplicatas usando Supabase
                response = supabase.table('ajuda').select('id').eq('nome', nome_normalizado).eq('telefone', telefone_formatado).execute()
                
                # Se 'response.data' não estiver vazia, um registro foi encontrado
                if response.data:
                    st.warning(f"Já existe um registro com o nome **{nome_normalizado}** e o telefone **{telefone_formatado}**.")
                else:
                    # Nenhuma duplicata encontrada, prosseguir com a inserção
                    
                    # --- LÓGICA DE DATA E HORA COM FUSO HORÁRIO DE BRASÍLIA ---
                    # 1. Define o fuso horário de Brasília/São Paulo
                    br_timezone = pytz.timezone('America/Sao_Paulo')
                    
                    # 2. Obtém a data e hora atuais já com o fuso horário aplicado.
                    # Este é o objeto que será enviado ao banco de dados.
                    data_hora_para_banco = datetime.now(br_timezone)
                    
                    # 3. Cria uma versão formatada da data apenas para exibição na mensagem de sucesso.
                    data_hora_display = data_hora_para_banco.strftime("%d/%m/%Y - %H:%M")

                    dados_para_inserir = {
                        "nome": nome_normalizado,
                        "tipo_pessoa": tipo_pessoa,
                        # Adiciona o campo de vínculo. Pode ser necessário criar essa coluna no Supabase.
                        "vinculo_descricao": vinculo_normalizado, 
                        "candidato_lideranca": candidato_normalizado,
                        "municipio": municipio_normalizado,
                        "telefone": telefone_formatado,
                        "tipo_ajuda": tipo_ajuda_normalizado,
                        "descricao_outros": descricao_normalizada,
                        "detalhes": detalhes_normalizados,
                        "quantidade": quantidade,
                        "valor": valor,
                        # ATUALIZADO: Enviando o objeto de data/hora com fuso horário
                        "data_hora": str(data_hora_para_banco) 
                    }
                    
                    insert_response = supabase.table('ajuda').insert(dados_para_inserir).execute()

                    # Verificar se a inserção foi bem-sucedida
                    if insert_response.data:
                        st.success(f"Registro criado com sucesso em {data_hora_display}\n\n" # ATUALIZADO: Usando a data formatada para display
                                     f"**Detalhes:**\n"
                                     f"- Nome: {nome_normalizado}\n"
                                     f"- Telefone: {telefone_formatado}")
                    else:
                        st.error(f"Ocorreu um erro ao salvar os dados. Detalhes: {insert_response.error.message}")

            except Exception as e:
                st.error(f"Ocorreu um erro na comunicação com o banco de dados. Por favor, verifique a conexão e as credenciais.")
                st.error(f"Detalhes do erro: {e}")
app()
