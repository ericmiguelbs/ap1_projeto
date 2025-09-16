# Usar imagem oficial do Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivo de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda a aplicação
COPY . .

# Variáveis de ambiente Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expor a porta 5000
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run"]