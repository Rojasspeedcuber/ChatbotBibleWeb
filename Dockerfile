FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 9000

# Define o comando para iniciar o Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=9000", "--server.address=0.0.0.0"]
