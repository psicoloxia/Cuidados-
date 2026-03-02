import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Archivos de base de datos
DB_FILE = "datos_cuidados.csv"
RECORDS_FILE = "recordatorios.csv"

# Funciones de persistencia
def cargar_datos(file, columns):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

def guardar_datos(df, file):
    df.to_csv(file, index=False)

# Configuración Visual
st.set_page_config(page_title="Plan de Cuidados ASPAS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    * { font-family: Arial, sans-serif; color: black !important; }
    h1, h2, h3, p, span, label { font-size: 1.2rem !important; }
    .alerta-roja { background-color: #ffcdd2; color: #b71c1c !important; padding: 15px; border-radius: 10px; font-weight: bold; border: 2px solid #b71c1c; font-size: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Carga de datos
df_reg = cargar_datos(DB_FILE, ["Nombre", "Fecha", "Hora", "Estado", "Sueño", "Depo", "Enema", "Uñas", "Obs"])
df_rec = cargar_datos(RECORDS_FILE, ["Nota"])

# Encabezado
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("Logo_ASPAS.gif"): st.image("Logo_ASPAS.gif", width=120)
    else: st.write("Logo no encontrado")
with col_titulo:
    st.title("Plan de Cuidados - Asociación ASPAS")

# Recordatorios
st.subheader("📌 Recordatorios")
with st.expander("Gestionar Recordatorios"):
    nueva_nota = st.text_input("Añadir nuevo recordatorio:")
    if st.button("Añadir"):
        if nueva_nota:
            df_rec = pd.concat([df_rec, pd.DataFrame([{"Nota": nueva_nota}])], ignore_index=True)
            guardar_datos(df_rec, RECORDS_FILE)
            st.rerun()
    for i, row in df_rec.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row['Nota']}")
        if c2.button("✅", key=f"del_{i}"):
            df_rec = df_rec.drop(i)
            guardar_datos(df_rec, RECORDS_FILE)
            st.rerun()

st.divider()

# Registro
if 'personas' not in st.session_state: st.session_state['personas'] = ["Selecciona...", "Usuario A"]
persona_sel = st.selectbox("👤 Nombre del Residente:", st.session_state['personas'])

if persona_sel != "Selecciona...":
    st.write(f"### Registrando para: **{persona_sel}**")
    emocional = st.selectbox("Estado Emocional", ["Estable", "Agitado", "Triste", "Alegre"])
    if emocional == "Agitado":
        st.markdown('<div class="alerta-roja">⚠️ ¡ATENCIÓN: ESTADO AGITADO! ⚠️</div>', unsafe_allow_html=True)

    with st.form("registro_diario", clear_on_submit=True):
        f_hoy = st.date_input("Fecha", datetime.now())
        c1, c2, c3 = st.columns(3)
        with c1: sueno = st.selectbox("Sueño", ["Sí", "No"])
        with c2: depo = st.selectbox("Deposiciones", ["Sí", "No"])
        with c3: enema = st.selectbox("Enema", ["Sí", "No"])
        uñas = st.selectbox("Corte de uñas", ["Sí", "No"])
        obs = st.text_area("Observaciones", max_chars=200)
        
        if st.form_submit_button("💾 GUARDAR REGISTRO"):
            hora_actual = datetime.now().strftime("%H:%M:%S")
            nuevo = pd.DataFrame([[persona_sel, f_hoy, hora_actual, emocional, sueno, depo, enema, uñas, obs]], columns=df_reg.columns)
            df_reg = pd.concat([df_reg, nuevo], ignore_index=True)
            guardar_datos(df_reg, DB_FILE)
            st.success(f"Guardado a las {hora_actual}")