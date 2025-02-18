FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 9000

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=9000
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Define o comando para iniciar o Streamlit
CMD ["streamlit", "run", "app.py"]
