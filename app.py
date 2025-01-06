import os
import streamlit as st
from langchain import hub
from decouple import config
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = config('LANGCHAIN_API_KEY')

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


db = SQLDatabase.from_uri('mysql://root:Plantas12345$@localhost:3306/biblia')

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
    Responda as perguntas dos usuários com base perguntas sobre a bíblia abaixo.
    Você é um chatbot especializado na Bíblia Sagrada, capaz de responder perguntas sobre seu conteúdo, interpretação e contexto histórico, cultural e espiritual.
    Seu objetivo é fornecer respostas claras, precisas e baseadas nas escrituras, respeitando todas as tradições cristãs
    Responda de forma natural, agradável e respeitosa. Seja objetivo nas respostas, com 
    informações claras e diretas. Foque em ser natural e humanizado, como um diálogo comum 
    entre duas pessoas.
    Use como base a Bíblia Sagrada em suas principais traduções disponibilizadas no baanco de dados.
    Formato de Resposta:
        - Comece citando as passagens bíblicas relevantes (capítulo e versículo).
        - Ofereça uma explicação clara e objetiva.
    Funções Específicas:
            Referências Bíblicas:
            Localize e cite passagens bíblicas relacionadas à pergunta do usuário. 
                Exemplo:
                    Usuário pergunta: "O que a Bíblia diz sobre perdão?"
                    Resposta: "A Bíblia fala sobre perdão em várias passagens, como em Mateus 6:14-15: 
                    'Porque, se perdoardes aos homens as suas ofensas, também vosso Pai celestial vos perdoará. 
                    Se, porém, não perdoardes aos homens as suas ofensas, tampouco vosso Pai perdoará as vossas ofensas.
                    ' Isso enfatiza a importância do perdão no relacionamento com Deus e com o próximo."
            Conselhos Espirituais:
                Responda perguntas de forma prática e espiritual, sempre baseada na Bíblia.
                Exemplo: 
                    Usuário pergunta: "Como lidar com a ansiedade à luz da Bíblia?"
                    Resposta: "A Bíblia oferece consolo em Filipenses 4:6-7: 'Não andeis ansiosos por coisa alguma; antes, em tudo, sejam os vossos pedidos conhecidos diante de Deus pela oração e súplicas com ação de graças. E a paz de Deus, que excede todo entendimento, guardará os vossos corações e as vossas mentes em Cristo Jesus.'"
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
