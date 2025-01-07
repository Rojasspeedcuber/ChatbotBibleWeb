import os
import streamlit as st
from langchain import hub
from decouple import config
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


def ask_question(model, query):
    llm = ChatGroq(model=model)
    system_prompt = '''
    Use o contexto para responder as perguntas.
    Se não encontrar uma resposta no contexto,
    explique que não há informações disponíveis.
    Responda em formato de markdown e com visualizações
    elaboradas e interativas.
    Use como base a Bíblia Sagrada disponibilizada no banco de dados.
    A resposta final deve ter uma formatação amigável(markdown) de vizualização para o usuário.
    Responda sempre em português brasileiro.
    Contexto: {context}
    '''

    messages = [('system', system_prompt, agent)]
    for message in st.session_state.messages:
        messages.append((message.get('role'), message.get('content')))
    messages.append(('human', '{input}'))

    response = agent.invoke({'input': 'query'})
    return response.get('answer')


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

st.set_page_config(
    page_title='Bible AI',
    page_icon='biblia.png'
)

st.header('Chatbot Gênesis')

model_options = [
    'llama-3.3-70b-versatile',
    'llama-3.1-8b-instant',
    'distil-whisper-large-v3-en',
    'mixtral-8x7b-32768',
]

selected_model = st.sidebar.selectbox(
    label='Selecione o modelo LLM',
    options=model_options,
)

st.sidebar.markdown('### Sobre')
st.sidebar.markdown('Sou o ChatBot Gênesis. Fui criado pela inspiração de Deus na vida de um estudante de Ciência da Computação. Utilizo Inteligência Artificial para ajudá-lo a conhecer os ensinamentos bíblicos.')
st.write('Faça perguntas sobre a Bíblia')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_question = st.chat_input('O que deseja saber sobre a Bíblia?')

model = ChatGroq(
    model=selected_model,
)


db = SQLDatabase.from_uri('sqlite:///NTLH.sqlite')

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model,
)

system_message = hub.pull('hwchase17/react')

agent = create_react_agent(
    llm=model,
    tools=toolkit.get_tools(),
    prompt=system_message,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)


if user_question:
    for message in st.session_state.messages:
        st.chat_message(message.get('role')).write(message.get('content'))

    st.chat_message('user').write(user_question)
    st.session_state.messages.append(
        {'role': 'user', 'content': user_question})
    with st.spinner('Buscando resposta...'):
        response = ask_question(
            model=selected_model,
            query=user_question,
            agent=agent_executor,
        )

        st.chat_message('ai').write(response)
        st.session_state.messages.append({'role': 'ai', 'content': response})
