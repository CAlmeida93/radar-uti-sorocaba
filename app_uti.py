import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Combate Biológico | UTI Tática", page_icon="🛡️", layout="wide")

# --- DADOS ESTRATÉGICOS (Tabelas 2 e 3 da Tese) ---
db_resistencia = {
    "Gram-Negativos": {
        "Acinetobacter baumannii": {"Meropenem": 96.6, "Ceftazidima": 95.0, "Cefepima": 96.6, "Amicacina": 81.7, "Polimixina B": 0.0},
        "Klebsiella pneumoniae": {"Meropenem": 91.3, "Ceftazidima": 91.1, "Cefepima": 92.8, "Amicacina": 32.6, "Polimixina B": 0.0},
        "Pseudomonas aeruginosa": {"Meropenem": 33.0, "Ceftazidima": 27.5, "Cefepima": 29.9, "Amicacina": 4.1, "Ciprofloxacino": 39.3},
        "Escherichia coli": {"Meropenem": 0.0, "Ceftriaxona": 54.1, "Ciprofloxacino": 58.6, "Amicacina": 5.8}
    },
    "Gram-Positivos": {
        "Staphylococcus aureus": {"Oxacilina": 40.9, "Vancomicina": 0.0, "Clindamicina": 46.9},
        "Staphylococcus haemolyticus": {"Oxacilina": 97.8, "Vancomicina": 0.0, "Linezolida": 0.0},
        "Enterococcus faecalis": {"Ampicilina": 1.7, "Vancomicina": 0.0, "Linezolida": 0.0},
        "Enterococcus faecium": {"Ampicilina": 100.0, "Vancomicina": 100.0, "Linezolida": 0.0}
    }
}

atb_gram_negativos = [
    "Meropenem", "Imipenem", "Ceftazidima", "Cefepima", "Ceftriaxona", 
    "Piperacilina-Tazobactam", "Amicacina", "Gentamicina", 
    "Ciprofloxacino", "Polimixina B", "Tigeciclina", "Ampicilina-Sulbactam"
]

atb_gram_positivos = [
    "Oxacilina", "Ampicilina", "Vancomicina", "Linezolida", "Teicoplanina", 
    "Clindamicina", "Daptomicina", "Eritromicina", "Ceftriaxona"
]

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ Combate Biológico: Assistente Tático UTI")
st.markdown("""
**Base de Dados:** Tese de Doutorado - UTI Santa Casa de Sorocaba
*Ferramenta de apoio à decisão baseada em epidemiologia local e PK/PD.*
""")

# --- MENU LATERAL ---
menu = st.sidebar.radio("Navegação Tática", [
    "🚨 Radar de Resistência", 
    "💊 Calculadora PK/PD de Precisão", 
    "📊 Tabela 6 (Visão Geral)"
])

# --- MÓDULO 1: RADAR DE RESISTÊNCIA ---
if menu == "🚨 Radar de Resistência":
    st.header("Antibiograma Digital Local")
    st.info("Selecione o patógeno isolado. Os dados representam a taxa de resistência histórica na unidade (Tabelas 2 e 3).")
    
    tipo_bacteria = st.selectbox("Tipo de Bactéria", ["Gram-Negativos", "Gram-Positivos"])
    bacteria = st.selectbox("Selecione o Microrganismo", list(db_resistencia[tipo_bacteria].keys()))
    
    st.subheader(f"Perfil de Resistência: *{bacteria}*")
    
    dados_bacteria = db_resistencia[tipo_bacteria][bacteria]
    lista_exibicao = atb_gram_negativos if tipo_bacteria == "Gram-Negativos" else atb_gram_positivos
    
    col1, col2 = st.columns(2)
    meio = len(lista_exibicao) // 2 + (len(lista_exibicao) % 2)
    
    def renderizar_cartao(antibiotico):
        if antibiotico in dados_bacteria:
            resist = dados_bacteria[antibiotico]
            cor = "green"
            msg = "✅ Sensibilidade Alta (Risco Baixo)"
            if resist > 20: 
                cor = "orange"
                msg = "⚠️ Cuidado (Resistência Moderada)"
            if resist > 50: 
                cor = "red"
                msg = "⛔ Alta Resistência (Evitar Empirismo)"
                
            return f"""
            <div style="padding:10px; border-radius:5px; border:1px solid #ddd; margin-bottom:10px; background-color:{'#e8f5e9' if cor=='green' else '#fff3e0' if cor=='orange' else '#ffebee'}">
                <strong>{antibiotico}</strong>: <span style="color:{cor}; font-size:1.2em; font-weight:bold">{resist}% Resistente</span><br>
                <small>{msg}</small>
            </div>
            """
        else:
            return f"""
            <div style="padding:10px; border-radius:5px; border:1px solid #ddd; margin-bottom:10px; background-color:#f8f9fa; color:#6c757d;">
                <strong>{antibiotico}</strong>: <span style="font-size:1.1em;">Sem dados / Não testado</span><br>
                <small>⚪ Consulte a CCIH da unidade</small>
            </div>
            """

    with col1:
        for atb in lista_exibicao[:meio]:
            st.markdown(renderizar_cartao(atb), unsafe_allow_html=True)
            
    with col2:
        for atb in lista_exibicao[meio:]:
            st.markdown(renderizar_cartao(atb), unsafe_allow_html=True)
            
    if bacteria in ["Klebsiella pneumoniae", "Acinetobacter baumannii"]:
        st.error("**ALERTA CRÍTICO DA TESE:** Resistência a Carbapenêmicos > 90%. Considere poupar Meropenem e avaliar terapias combinadas conforme protocolo da CCIH.")

# --- MÓDULO 2: CALCULADORA PK/PD (NOVO FORMATO) ---
elif menu == "💊 Calculadora PK/PD de Precisão":
    st.header("Otimização Farmacocinética (PK/PD)")
    st.markdown("Selecione o antimicrobiano para visualizar o alvo farmacodinâmico e a posologia recomendada.")
    
    lista_pkpd = [
        "Beta-lactâmicos (Meropenem, Cefepima, Ceftazidima)", 
        "Aminoglicosídeos (Amicacina, Gentamicina)", 
        "Teicoplanina", 
        "Vancomicina", 
        "Polimixina B", 
        "Fluoroquinolonas (Cipro/Levofloxacino)"
    ]
    
    drug = st.selectbox("Escolha a Classe / Antimicrobiano", lista_pkpd)
    
    st.markdown("---")
    
    if drug == "Beta-lactâmicos (Meropenem, Cefepima, Ceftazidima)":
        st.subheader("🎯 Alvo: **T > MIC** (Tempo acima da MIC)")
        st.markdown("*O objetivo é manter a concentração do antibiótico no sangue acima da Concentração Inibitória Mínima pelo maior tempo possível entre as doses.*")
        st.success("✅ Posologia Estratégica: **Infusão Estendida (3 a 4 horas)** ou **Infusão Contínua**.")
        st.info("Aumentar a dose em bolus rápido não melhora a eficácia. O segredo é prolongar o tempo de gotejamento na bomba de infusão (especialmente se ClCr > 50 mL/min).")

    elif drug == "Aminoglicosídeos (Amicacina, Gentamicina)":
        st.subheader("🎯 Alvo: **Cmax / MIC** (Pico de Concentração Máxima)")
        st.markdown("*O objetivo é atingir um pico de concentração muito alto, rápido e transitório, para gerar morte bacteriana imediata e evitar toxicidade renal prolongada.*")
        st.success("✅ Posologia Estratégica: **1x ao dia** (Dose Única Diária).")
        st.info("Evite fracionar a dose (ex: de 12/12h). Calcule a dose total pelo peso (ex: Amicacina 25mg/kg) e administre de uma só vez.")

    elif drug == "Teicoplanina":
