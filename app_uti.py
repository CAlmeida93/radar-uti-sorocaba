import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Combate Biológico | UTI Tática", page_icon="🛡️", layout="wide")

# --- DADOS ESTRATÉGICOS (Baseados nas Tabelas 2, 3 e 5 da Tese) ---
# Resistência (%) extraída da Tese Final Revisada
db_resistencia = {
    "Gram-Negativos": {
        "Klebsiella pneumoniae": {"Meropenem": 91.3, "Ceftazidima": 91.1, "Cefepima": 92.8, "Amicacina": 32.6, "Polimixina B": 0.0},
        "Acinetobacter baumannii": {"Meropenem": 96.6, "Ceftazidima": 95.0, "Cefepima": 96.6, "Amicacina": 81.7, "Polimixina B": 0.0},
        "Pseudomonas aeruginosa": {"Meropenem": 33.0, "Ceftazidima": 27.5, "Cefepima": 29.9, "Amicacina": 4.1, "Ciprofloxacino": 39.3},
        "Escherichia coli": {"Meropenem": 0.0, "Ceftriaxona": 54.1, "Ciprofloxacino": 58.6, "Amicacina": 5.8},
    },
    "Gram-Positivos": {
        "Staphylococcus aureus": {"Oxacilina (MRSA)": 40.9, "Vancomicina": 0.0, "Clindamicina": 46.9},
        "Staphylococcus haemolyticus": {"Oxacilina": 97.8, "Vancomicina": 0.0, "Linezolida": 0.0},
        "Enterococcus faecalis": {"Ampicilina": 1.7, "Vancomicina": 0.0, "Linezolida": 0.0},
        "Enterococcus faecium": {"Ampicilina": 100.0, "Vancomicina": 100.0, "Linezolida": 0.0}
    }
}

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ Combate Biológico: Assistente Tático UTI")
st.markdown("""
**Base de Dados:** Tese de Doutorado - UTI Santa Casa de Sorocaba (2025)
*Ferramenta de apoio à decisão baseada em epidemiologia local e PK/PD.*
""")

# Menu Lateral
menu = st.sidebar.radio("Navegação Tática", ["🚨 Radar de Resistência", "💊 Calculadora PK/PD de Precisão", "📋 Protocolo Empírico"])

# --- MÓDULO 1: RADAR DE RESISTÊNCIA (Heatmap Interativo) ---
if menu == "🚨 Radar de Resistência":
    st.header("Antibiograma Digital Local")
    st.info("Dados baseados nas Tabelas 2 e 3 da tese. Selecione o patógeno isolado na cultura.")
    
    tipo_bacteria = st.selectbox("Tipo de Bactéria", ["Gram-Negativos", "Gram-Positivos"])
    bacteria = st.selectbox("Selecione o Microrganismo", list(db_resistencia[tipo_bacteria].keys()))
    
    st.subheader(f"Perfil de Resistência: *{bacteria}*")
    
    col1, col2 = st.columns(2)
    
    dados = db_resistencia[tipo_bacteria][bacteria]
    
    # Exibição visual com cartões coloridos
    for antibiotico, resist in dados.items():
        cor = "green"
        msg = "✅ Opção Segura"
        if resist > 20: 
            cor = "orange"
            msg = "⚠️ Cuidado (Risco Moderado)"
        if resist > 50: 
            cor = "red"
            msg = "⛔ Alta Resistência (Evitar Monoterapia)"
            
        with st.container():
            st.markdown(f"""
            <div style="padding:10px; border-radius:5px; border:1px solid #ddd; margin-bottom:10px; background-color:{'#e8f5e9' if cor=='green' else '#fff3e0' if cor=='orange' else '#ffebee'}">
                <strong>{antibiotico}</strong>: <span style="color:{cor}; font-size:1.2em; font-weight:bold">{resist}% de Resistência</span><br>
                <small>{msg}</small>
            </div>
            """, unsafe_allow_html=True)
            
    if bacteria == "Klebsiella pneumoniae" or bacteria == "Acinetobacter baumannii":
        st.error("**ALERTA CRÍTICO:** Resistência a Carbapenêmicos > 90%. Considere poupar Meropenem e avaliar terapias combinadas (ex: Polimixina B ou novos inibidores de beta-lactamase) conforme CCIH.")

# --- MÓDULO 2: CALCULADORA PK/PD (Correção de Doses) ---
elif menu == "💊 Calculadora PK/PD de Precisão":
    st.header("Otimização Farmacocinética (PK/PD)")
    st.warning("A tese identificou que apenas **58% das doses de Meropenem** e **25% de Amicacina** atingiram o alvo ideal na unidade. Use esta ferramenta para corrigir.")
    
    drug = st.selectbox("Escolha o Antimicrobiano", ["Meropenem (T>MIC)", "Amicacina (Cmax/MIC)"])
    
    if drug == "Meropenem (T>MIC)":
        st.markdown("### Otimização de Beta-Lactâmicos")
        peso = st.number_input("Peso do Paciente (kg)", value=70)
        clearence = st.number_input("ClCr Estimado (mL/min)", value=80)
        
        st.markdown("---")
        if clearence > 50:
            st.success("✅ **Recomendação Tática:** Infusão Estendida")
            st.markdown(f"""
            Para garantir **40% a 100% do tempo acima da MIC (T>MIC)** nesta unidade:
            - **Dose:** 1g ou 2g a cada 8h.
            - **Método:** Diluir em 100mL e infundir em **3 a 4 horas** (bomba de infusão).
            - *Justificativa:* O bolus rápido (30 min) falhou em 41% dos casos analisados na tese.
            """)
        else:
            st.warning("⚠️ Ajuste renal necessário. Consulte farmacêutico clínico, mas MANTENHA a infusão estendida se possível.")

    elif drug == "Amicacina (Cmax/MIC)":
        st.markdown("### Otimização de Aminoglicosídeos")
        peso = st.number_input("Peso do Paciente (kg)", value=70)
        
        st.markdown("---")
        dose_ideal = peso * 25 # 25 a 30mg/kg
        st.success(f"✅ **Dose Sugerida:** {dose_ideal:.0f} mg (Dose Única Diária)")
        st.markdown("""
        - **Estratégia:** Dose única elevada para maximizar o pico (Cmax/MIC).
        - **Erro Comum na Unidade:** Evite fracionar a dose (ex: 500mg a cada 12h), pois isso reduz a eficácia bactericida e aumenta a nefrotoxicidade.
        """)

# --- MÓDULO 3: PROTOCOLO EMPÍRICO ---
elif menu == "📋 Protocolo Empírico":
    st.header("Guia de Decisão Empírica")
    st.markdown("Baseado na prevalência local de patógenos (Tabela 1 da Tese).")
    
    sindrome = st.selectbox("Síndrome Clínica", ["Pneumonia Associada à Ventilação (PAV)", "Infecção de Corrente Sanguínea (Sepse)", "Infecção Urinária (Sonda)"])
    
    if sindrome == "Pneumonia Associada à Ventilação (PAV)":
        st.markdown("""
        **Principais Inimigos (Top 3):**
        1. *Acinetobacter baumannii* (Alta Resistência)
        2. *Klebsiella pneumoniae* (Produtora de KPC/ESBL)
        3. *Pseudomonas aeruginosa*
        
        **Recomendação Tática:**
        - Evitar Cefepima ou Meropenem em monoterapia (Resistência >90% para os dois primeiros).
        - **Sugestão:** Considerar Polimixina B + Meropenem (efeito sinérgico ou 'isca') ou Ceftazidima-Avibactam se disponível.
        """)
        
    elif sindrome == "Infecção de Corrente Sanguínea (Sepse)":
        st.markdown("""
        **Principais Inimigos:**
        - Gram-Positivos (CoNS) são muito frequentes.
        - *Klebsiella pneumoniae*.
        
        **Recomendação Tática:**
        - **Gram-Positivos:** Vancomicina é segura (0% resistência), mas Oxacilina tem falha >90% para *S. haemolyticus*.
        - **Gram-Negativos:** A *Klebsiella* local tem alta resistência a Cefalosporinas de 3ª geração.
        """)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("**Combate Biológico v1.0**\nDesenvolvido para análise epidemiológica institucional.")