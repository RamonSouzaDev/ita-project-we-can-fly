# Dockerfile
# Imagem Oficial leve para o Web App do Agente
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências necessárias para Flask e Vertex AI GC SDK
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask google-genai gunicorn

# Copiar a arquitetura do agente
COPY src/ /app/src/

# Configurar variáveis de Ambiente Padrão
ENV PORT=8080
ENV GOOGLE_CLOUD_PROJECT=ita-wecanfly-v2-dev
ENV GOOGLE_CLOUD_LOCATION=us-central1

# Expor a porta 8080
EXPOSE 8080

# Comando para Iniciar o motor Gunicorn na nuvem
CMD ["gunicorn", "-b", "0.0.0.0:8080", "src.agent_cloud_engine:app"]
