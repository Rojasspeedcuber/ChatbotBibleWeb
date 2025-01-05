import os
import streamlit as st
import mysql.connector
from langchain import hub
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq

os.environ['GROQ_API_KEY'] = 'GROQ_API_KEY'


st.set_page_config(
    page_title='Bible AI',
    page_icon='biblia.png'
)

st.header('Chatbot Gênesis')

model_options = [
    'llama-3.3-70b-versatile',
    'llama-3.1-70b-versatile',
    'llama-3.1-8b-instant',
]

selected_box = st.sidebar.selectbox(
    label='Selecione o modelo LLM',
    options=model_options,
)

st.sidebar.markdown('### Sobre')
st.sidebar.markdown('Sou o ChatBot Gênesis. Fui criado pela inspiração de Deus na vida de um estudante de Ciência da Computação. Utilizo Inteligência Artificial para ajudá-lo a conhecer os ensinamentos bíblicos.')

st.write('Faça perguntas sobre a Bíblia')
user_question = st.text_input('O que deseja saber sobre a Bíblia?')


model = ChatGroq(
    model=selected_box,
)

db = SQLDatabase.from_uri('mysql:///biblia_13V.sql')
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)
system_message = hub.pull('hwchase/react')

if st.button('Enviar'):
    if user_question:
        st.write('FEZ UMA PERGUNTA!')
    else:
        st.warning('Por favor, insira uma pergunta.')
