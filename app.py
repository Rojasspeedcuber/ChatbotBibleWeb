import os
import streamlit as st
import mercadopago
from decouple import config
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from payments.page import exibir_link_pagamento
from payments.service import ACCESS_TOKEN

st.set_page_config(page_title='Bible AI', page_icon='biblia.png')


# 🔹 Configurando API Key do OpenAI para o Chatbot
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

# Função que exibe a interface de pagamento


def exibir_interface_pagamento():
    st.header("Pagamento Pendentes")
    st.write("Por favor, complete o pagamento para continuar.")
    # Exibe o link para o pagamento
    exibir_link_pagamento()


def verificar_pagamento(preference_id):
    # Configura a chave de acesso do Mercado Pago
    # A chave de acesso do Mercado Pago
    mp = mercadopago.SDK(ACCESS_TOKEN)

    # Verifica o status do pagamento utilizando o ID da preferência
    preference = mp.payment().get(preference_id)

    # O status de pagamento pode ser "approved", "pending", "rejected", etc.
    if preference['response']['status'] == 'approved':
        return True  # Pagamento aprovado
    else:
        return False  # Pagamento não aprovado


# Função principal para o chatbot bíblico


def main():
    """Executa a lógica principal do Chatbot Bíblico."""

    # ID da preferência do pagamento, normalmente vindo de uma transação
    preference_id = st.session_state.get('preference_id')

    if not preference_id or not verificar_pagamento(preference_id):
        # Se o pagamento não foi confirmado, exibe a interface de pagamento
        exibir_interface_pagamento()
        return  # Não executa o restante do código

    # 🔹 Se o pagamento foi confirmado, exibe a interface do chatbot
    st.header('Chatbot Gênesis')

    # 🔹 Modelos disponíveis para o Chatbot
    model_options = ['gpt-4', 'gpt-4-turbo', 'gpt-4o-mini', 'gpt-4o']
    bible_options = ['ACF', 'ARA', 'ARC', 'AS21',
                     'KJA', 'NAA', 'NTLH', 'NVI', 'NVT']

    selected_box = st.sidebar.selectbox(
        label='Selecione o modelo LLM', options=model_options)
    selected_bible = st.sidebar.selectbox(
        label='Selecione a versão da base de dados', options=bible_options)

    # 🔹 Informações sobre o Chatbot
    st.sidebar.markdown("### Sobre")
    st.sidebar.markdown(
        "Sou o ChatBot Gênesis. Fui criado pela inspiração de Deus na vida de um estudante de Ciência da Computação. "
        "Utilizo Inteligência Artificial para ajudá-lo a conhecer os ensinamentos bíblicos."
    )

    st.write("Faça perguntas sobre a Bíblia")

    # 🔹 Histórico de mensagens
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # 🔹 Input do usuário
    user_question = st.chat_input('O que deseja saber sobre a Bíblia?')

    # 🔹 Configuração do modelo e banco de dados
    model = ChatOpenAI(model=selected_box,
                       max_completion_tokens=1000, streaming=True)

    try:
        db = SQLDatabase.from_uri(f'sqlite:///databases/{selected_bible}.db')
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return

    toolkit = SQLDatabaseToolkit(db=db, llm=model)

    system_message = hub.pull('hwchase17/react')

    agent = create_react_agent(
        llm=model, tools=toolkit.get_tools(), prompt=system_message)
    agent_executor = AgentExecutor(
        agent=agent, tools=toolkit.get_tools(), handle_parsing_errors=True)

    # 🔹 Template de prompt para o Chatbot
    prompt = """
        Você é um chatbot especializado na Bíblia Sagrada, capaz de responder perguntas sobre seu conteúdo, 
        interpretação e contexto histórico, cultural e espiritual.
        Seu objetivo é fornecer respostas claras, precisas e baseadas nas escrituras, respeitando todas as tradições cristãs.
        Responda de forma natural, agradável e respeitosa. Seja objetivo nas respostas, com 
        informações claras e diretas. Foque em ser natural e humanizado, como um diálogo comum.
        Use como base a Bíblia Sagrada disponibilizada no banco de dados.
        Sempre use os versículos contidos na base de dados para responder as perguntas.
        A resposta final deve ter uma formatação amigável (markdown) para visualização do usuário.
        Responda sempre em português brasileiro.
        Pergunta: {q}
    """
    prompt_template = PromptTemplate.from_template(prompt)

    # 🔹 Se houver pergunta, processa a resposta
    if user_question:
        for message in st.session_state.messages:
            st.chat_message(message.get('role')).write(message.get('content'))

        st.chat_message('user').write(user_question)
        st.session_state.messages.append(
            {'role': 'user', 'content': user_question})

        with st.spinner('Buscando resposta...'):
            formatted_prompt = prompt_template.format(q=user_question)
            output = agent_executor.invoke({'input': formatted_prompt})
            st.markdown(output.get('output'))


# 🔹 Executando o aplicativo
if __name__ == '__main__':
    main()
