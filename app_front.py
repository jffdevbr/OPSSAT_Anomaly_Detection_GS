import os
import streamlit as st
import requests

st.set_page_config(page_title="Previsão de Anomalia", page_icon="📊")
st.title("📊 Previsão de Anomalia")
st.write("Insira os dados do segmento curto de sinal para prever o risco de anomalia.")

url_api = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

with st.form("form_features"):
    col1, col2 = st.columns(2)

# Valores do segmento 2058 - que é anomalo
    with col1:
        sampling = st.number_input("sampling", value=5)
        duration = st.number_input("duration", value=243)
        mean = st.number_input("mean", value=-0.000009)
        var = st.number_input("var", value=0.0000000002183395)
        kurtosis = st.number_input("kurtosis", value=-1.248399)
        
    with col2:
        skew = st.number_input("skew", value=-0.182327)
        n_peaks = st.number_input("n_peaks", value=2)
        smooth10_n_peaks = st.number_input("smooth10_n_peaks", value=1)
        smooth20_n_peaks = st.number_input("smooth20_n_peaks", value=1)
        diff_peaks = st.number_input("diff_peaks", value=1)
        diff_var = st.number_input("diff_var", value=0.00000000005188895)
        gaps_squared = st.number_input("gaps_squared", value=1219)
        channel_enc = st.number_input("channel_enc", value=0)
        
    submit_button = st.form_submit_button(label="🔮 Prever Risco")

if submit_button:
    dados_para_api = {
        "sampling": int(sampling),
        "duration": int(duration),
        "mean": float(mean),
        "var": float(var),
        "kurtosis": float(kurtosis),
        "skew": float(skew),
        "n_peaks": int(n_peaks),
        "smooth10_n_peaks": int(smooth10_n_peaks),
        "smooth20_n_peaks": int(smooth20_n_peaks),
        "diff_peaks": int(diff_peaks),
        "diff_var": float(diff_var),
        "gaps_squared": int(gaps_squared),
        "channel_enc": int(channel_enc)
    }
    
    try:
        with st.spinner('Analisando perfil do cliente...'):
            resposta = requests.post(url_api, json=dados_para_api, timeout=10)
            
            if resposta.status_code == 200:
                resultado = resposta.json()
                if resultado["anomalia"]:
                    st.error(f"⚠️ {resultado['mensagem']}")
                else:
                    st.success(f"✅ {resultado['mensagem']}")
            else:
                st.warning(f"Erro na API. Status Code: {resposta.status_code}")
                st.write(resposta.json())
                
    except requests.exceptions.ConnectionError:
        st.error(f"Erro de conexão: não foi possível alcançar a API em {url_api}. O container da API está rodando?")
    except requests.exceptions.Timeout:
        st.error("Tempo limite excedido. A API demorou muito para responder.")
