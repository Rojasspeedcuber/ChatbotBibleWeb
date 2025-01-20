FROM python:3.11-slim

WORKDIR /ChatbotBibleWeb

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=5000"]

EXPOSE 5000


