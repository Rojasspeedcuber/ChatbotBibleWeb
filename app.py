import os
import streamlit as st
from langchain import hub
from decouple import config
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

st.set_page_config(
    page_title='Bible AI',
    page_icon='biblia.png'
)

st.header('Chatbot Gênesis')

model_options = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o',
]

selected_box = st.sidebar.selectbox(
    label='Selecione o modelo LLM',
    options=model_options,
)

st.sidebar.markdown('### Sobre')
st.sidebar.markdown('Sou o ChatBot Gênesis. Fui criado pela inspiração de Deus na vida de um estudante de Ciência da Computação. Utilizo Inteligência Artificial para ajudá-lo a conhecer os ensinamentos bíblicos.')

st.write('Faça perguntas sobre a Bíblia')
user_question = st.text_input('O que deseja saber sobre a Bíblia?')


model = ChatOpenAI(
    model=selected_box,
)


db = SQLDatabase.from_uri('NTLH.sqlite')

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

prompt = '''
    Use como base a Bíblia Sagrada disponibilizada no banco de dados.
        A resposta final deve ter uma formatação amigável(markdown) de vizualização para o usuário.
        Responda sempre em português brasileiro.
        Pergunta: {q}
    '''
prompt_template = PromptTemplate.from_template(prompt)


if st.button('Enviar'):
    if user_question:
        with st.spinner('Consultando banco de dados...'):
            formatted_prompt = prompt_template.format(q=user_question)
            output = agent_executor.invoke({'input': formatted_prompt})
            st.markdown(output.get('output'))
    else:
        st.warning('Por favor, insira uma pergunta.')
