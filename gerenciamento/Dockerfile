# Dockerfile CORRIGIDO
FROM python:3.11-slim
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO o código da pasta atual para o workdir /app
# (O .dockerignore vai garantir que os arquivos desnecessários não sejam copiados)
COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]