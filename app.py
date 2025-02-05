import os
import streamlit as st
import mercadopago
from fastapi import FastAPI, Request, BackgroundTasks
import requests
import threading
import uvicorn
import logging
from decouple import config
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from payments.page import exibir_interface_pagamento
from payments.service import verificar_assinatura

st.set_page_config(page_title='Bible AI', page_icon='biblia.png')

# 🔹 Configuração do Logging
logging.basicConfig(filename="webhook.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# 🔹 Configuração da API FastAPI para Webhooks
app = FastAPI()

# 🔹 Configuração do Mercado Pago
ACCESS_TOKEN = config('MERCADO_PAGO_ACCESS_TOKEN')

# 🔹 Lista para armazenar eventos de Webhooks no Streamlit
if "webhook_events" not in st.session_state:
    st.session_state["webhook_events"] = []


def consultar_pagamento(payment_id):
    """Consulta detalhes do pagamento no Mercado Pago."""
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pagamento = response.json()
        logging.info(f"Pagamento {payment_id} consultado: {pagamento}")
        st.session_state["webhook_events"].append(pagamento)
    else:
        logging.error(
            f"Erro ao consultar pagamento {payment_id}: {response.text}")


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """Recebe notificações do Mercado Pago e processa os eventos."""
    data = await request.json()
    logging.info(f"Webhook recebido: {data}")

    if data.get("action") == "payment.created":
        payment_id = data["data"]["id"]
        logging.info(f"Novo pagamento recebido: {payment_id}")
        st.session_state["webhook_events"].append(
            {"status": "Recebido", "id": payment_id})

        # Processa o pagamento em background
        background_tasks.add_task(consultar_pagamento, payment_id)

    return {"status": "ok"}

# 🔹 Iniciar o servidor FastAPI em uma thread separada


def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8501)


thread = threading.Thread(target=start_api, daemon=True)
thread.start()

# 🔹 Função principal do Chatbot Bíblico


def main():
    """Executa a lógica principal do Chatbot Bíblico."""

    preference_id = st.session_state.get('preapproval_id')

    if not preference_id or not verificar_assinatura(preference_id):
        exibir_interface_pagamento()
        return

    st.header('Chatbot Gênesis')

    model_options = ['gpt-4', 'gpt-4-turbo', 'gpt-4o-mini', 'gpt-4o']
    bible_options = ['ACF', 'ARA', 'ARC', 'AS21',
                     'KJA', 'NAA', 'NTLH', 'NVI', 'NVT']

    selected_box = st.sidebar.selectbox(
        label='Selecione o modelo LLM', options=model_options)
    selected_bible = st.sidebar.selectbox(
        label='Selecione a versão da base de dados', options=bible_options)

    st.sidebar.markdown("### Sobre")
    st.sidebar.markdown(
        "Sou o ChatBot Gênesis. Fui criado pela inspiração de Deus na vida de um estudante de Ciência da Computação. "
        "Utilizo Inteligência Artificial para ajudá-lo a conhecer os ensinamentos bíblicos."
    )

    st.write("Faça perguntas sobre a Bíblia")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    user_question = st.chat_input('O que deseja saber sobre a Bíblia?')

    model = ChatOpenAI(model=selected_box, streaming=True)

    try:
        db = SQLDatabase.from_uri(
            f'sqlite:///databases/{selected_bible}.sqlite')
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return

    toolkit = SQLDatabaseToolkit(db=db, llm=model)

    system_message = hub.pull('hwchase17/react')

    agent = create_react_agent(
        llm=model, tools=toolkit.get_tools(), prompt=system_message)
    agent_executor = AgentExecutor(
        agent=agent, tools=toolkit.get_tools(), handle_parsing_errors=True)

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

    # 🔹 Seção para exibir Webhooks recebidos
    st.subheader("📋 Eventos Recebidos do Mercado Pago")
    for event in st.session_state["webhook_events"]:
        st.json(event)


# 🔹 Executando o aplicativo
if __name__ == '__main__':
    main()
