from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="API de Previsão de Anomalias OPSSAT",
    description="Endpoint para prever a anomalia usando o modelo RandomForest."
)

modelo = joblib.load('modelo_opssat.pkl')

class OpssatData(BaseModel):
    sampling: int
    duration: int
    mean: float
    var: float
    kurtosis: float
    skew: float
    n_peaks: int
    smooth10_n_peaks: int
    smooth20_n_peaks: int
    diff_peaks: int
    diff_var: float
    gaps_squared: int
    channel_enc: int


@app.post("/predict")
def prever(opssat: OpssatData):
    dados_dicionario = opssat.model_dump()
    
    # Criando o DataFrame com as colunas minúsculas exatas
    df = pd.DataFrame([dados_dicionario])
    
    try:
        # Agora o DataFrame casa perfeitamente com os nomes esperados
        previsao = modelo.predict(df)
        resultado = int(previsao[0])
        
        if resultado == 1:
            return {"anomalia": True, "mensagem": "Alerta: Alto risco de anomalia!"}
        else:
            return {"anomalia": False, "mensagem": "Baixo risco de anomalia."}
            
    except Exception as e:
        return {"anomalia": False, "mensagem": f"Erro na inferência do modelo: {str(e)}"}