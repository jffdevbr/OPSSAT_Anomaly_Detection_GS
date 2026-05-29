# ─────────────────────────────────────────────
# Container Principal — API de Previsão de anomalia
# FastAPI + XGBoost (Python 3.13)
# ─────────────────────────────────────────────
FROM python:3.13-slim

# Metadados da imagem
LABEL maintainer="jff2006br@gmail.com"
LABEL description="API de previsão de anomalia com FastAPI e Random Forest"
LABEL version="1.0"

# Diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/modelo_opssat.pkl \
    APP_PORT=8000

# Instala dependências do sistema necessárias para o XGBoost/scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação e o modelo treinado
COPY api.py .
COPY modelo_opssat.pkl .

# Expõe a porta da API
EXPOSE 8000

# Healthcheck: verifica se a API está respondendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

# Comando de inicialização
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
