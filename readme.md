# 🐳 Docker — Sistema de Previsão de anomalia

## Estrutura dos arquivos

```
projeto/
├── Dockerfile            # Container principal (API FastAPI)
├── Dockerfile.frontend   # Container de apoio (Dashboard Streamlit)
├── docker-compose.yml    # Orquestração dos dois containers
├── .env                  # Variáveis de ambiente
├── api.py                # Código da API
├── app_front.py          # Código do frontend
├── requirements.txt      # Dependências Python
└── modelo_opssat.pkl      # Modelo treinado (necessário!)
```

---

## Como executar


### 1. Subir os dois containers
```bash
docker compose up --build
```

### 2. Acessar as aplicações
| Serviço   | URL                          |
|-----------|------------------------------|
| Dashboard | http://localhost:8501        |
| API docs  | http://localhost:8000/docs   |
| API JSON  | http://localhost:8000/predict|

* Para testar o predict via terminal (bash):

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sampling": 5,
    "duration": 243,
    "mean": -0.000009,
    "var": 0.0000000002183395,
    "kurtosis": -1.248399,
    "skew": -0.182327,
    "n_peaks": 2,
    "smooth10_n_peaks": 1,
    "smooth20_n_peaks": 1,
    "diff_peaks": 1,
    "diff_var": 0.00000000005188895,
    "gaps_squared": 1219,
    "channel_enc": 0
  }'
```

### 3. Parar os containers
```bash
docker compose down
```

### 4. Parar e remover volumes
```bash
docker compose down -v
```

---

## Comandos úteis

```bash
# Ver logs de todos os containers
docker compose logs -f

# Ver logs só da API
docker compose logs -f api

# Ver logs só do frontend
docker compose logs -f frontend

# Rebuildar apenas um serviço
docker compose up --build api

# Ver status dos containers
docker compose ps
```

---