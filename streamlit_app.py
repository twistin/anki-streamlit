import streamlit as st
import os
from pathlib import Path
import openai

# Configuración de la API (puedes usar st.secrets en Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

# Prompt base personalizado
BASE_PROMPT = """
A partir del siguiente texto, genera tarjetas tipo Anki que ayuden a estudiar sus conceptos clave. Cada tarjeta debe tener una pregunta y una respuesta.
Las preguntas deben centrarse en definiciones, relaciones conceptuales, contexto histórico y ejemplos relevantes. El formato debe ser:

Pregunta:
...
Respuesta:
...

Texto:
"""

# Función para generar tarjetas con OpenAI
def generar_tarjetas(texto):
    prompt = BASE_PROMPT + texto
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un generador de tarjetas educativas tipo Anki."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar tarjetas: {e}"

# Interfaz en Streamlit
st.title("Generador de Tarjetas Anki desde Notas de Obsidian")

modo = st.radio("Selecciona origen de las notas:", ("Local (ruta completa)", "Repositorio para nube"))

if modo == "Local (ruta completa)":
    ruta_personal = "/Users/sdcarr/Documents/UNED-investigacion/INVESTIGACION-NOTAS/04_NOTAS_ATÓMICAS"
else:
    ruta_personal = "notes"

notes_dir = Path(ruta_personal)

if not notes_dir.exists():
    st.warning(f"La carpeta '{notes_dir}' no existe. Asegúrate de que esté disponible.")
else:
    archivos = list(notes_dir.glob("*.md")) + list(notes_dir.glob("*.txt"))
    if archivos:
        archivo_seleccionado = st.selectbox("Selecciona una nota:", archivos)
        texto = Path(archivo_seleccionado).read_text(encoding="utf-8")
        st.text_area("Contenido de la nota:", texto, height=300)

        if st.button("Generar tarjetas Anki"):
            with st.spinner("Generando tarjetas..."):
                tarjetas = generar_tarjetas(texto)
                st.markdown("### Tarjetas generadas")
                st.text_area("Resultado:", tarjetas, height=400)
    else:
        st.info(f"No hay archivos .md o .txt en la carpeta '{notes_dir}'.")
