import streamlit as st
import re

# Configuración de la página
st.set_page_config(
    page_title="Generador de HTML",
    page_icon="📄",
    layout="centered"
)

def rellenar_plantilla(template, datos):
    """Reemplaza los placeholders {{}} con los datos proporcionados"""
    resultado = template
    for key, value in datos.items():
        placeholder = f"{{{{{key}}}}}"
        resultado = resultado.replace(placeholder, str(value))
    return resultado

def extraer_placeholders(template):
    """Devuelve una lista de placeholders en el orden en que aparecen, sin duplicados"""
    placeholders = []
    for match in re.finditer(r"{{\s*([\w\s-]+)\s*}}", template):
        ph = match.group(1).strip()
        if ph not in placeholders:
            placeholders.append(ph)
    return placeholders

# Diccionario con las descripciones del contenido correcto de los placeholders
PLACEHOLDER_INFO = {
    "MesYAno": "Mes y año del material de divulgación, no del estudio",
    "Introduccion": "Introduccion breve para generar curiosidad o presentar adecuadamente el estudio",
    "TituloEstudio": "Título real de la investigación",
    "Autorxs": "Lista de autorxs en una sola línea",
    "Doi": "DOI del artículo o publicación (sólo números). Por ejemplo: 10.1186/s12978‑025‑02036‑8",
    "Fig1Url": "Enlace público de la imagen ilustrativa principal. Es una url que devuelve solamente la imagen original. El formato correcto suele terminar con la extensión del archivo.",
    "Fig1Pie": "Pie de la figura 1",
    "Credito1Url": "Enlace de la página de la fuente original para la figura 1. Puede ser un blog, página de wikipedia, etc. Cualquier enlace que remita a la fuente original.",
    "Credito1": "Texto para dar crédito a la fuente original de la figura 1",
    "Metodos": "Métodos descritos en 3-4 oraciones",
    "Fecha": "Fecha o periodo de fechas que cubre la investigación",
    "Lugar": "Sitio o sitios de estudio",
    "Muestra": "Tamaño de muestra de la investigación",
    "Resultado": "Resultados principales de la investigación en 4-5 oraciones",
    "Fig2Url": "Enlace púbico de la imagen ilustrativa de los resultados, como una gráfica o una tabla. Es una url que devuelve solamente la imagen original. El formato correcto suele terminar con la extensión del archivo.",
    "Fig2Pie": "Pie de la figura 2",
    "Importancia": "Explicación de la importancia para la justicia reproductiva en 3-4 oraciones",
    "Fig3Url": "Enlace públic de imagen ilustrativa de la importancia para la justicia reproductiva. Es una url que devuelve solamente la imagen original. El formato correcto suele terminar con la extensión del archivo.",
    "Fig3Pie": "Pie de la figura 3",
    "Credito3": "Texto para dar crédito a la fuente original de la figura 3",
    "Credito3Url": "Enlace de referencia a la fuente original de la figura 3. Puede ser un blog, página de wikipedia, etc. Cualquier enlace que remita a la fuente original.",
    "RecomendacionPolitica": "Recomendación en términos de postura política en 1-2 oraciones",
    "RecomendacionProgramas": "Recomendación en términos de programas 2 en 1-2 oraciones",
    "RecomendacionInvestigacion": "Recomendación en términos de investigación futura 3 en 1-2 oraciones",
    "CitaFormateada": "Cita correcta",
    "EnlaceEstudio": "Enlace al sitio del estudio original"
}

# --- Interfaz ---
st.title("📄 Generador de HTML")
st.markdown("""
Sube tu plantilla HTML con placeholders (por ejemplo `{{nombre}}`, `{{email}}`) y completa los campos generados automáticamente.  
Podrás ver una vista previa del documento antes de descargarlo.
""")

st.divider()

# Subida de archivo
st.subheader("1. Sube tu plantilla HTML")
template_file = st.file_uploader(
    "Selecciona tu archivo de plantilla",
    type=['html'],
    help="Tu plantilla debe contener placeholders como {{nombre}}, {{email}}, etc."
)

# Ejemplo opcional
with st.expander("Ejemplo de plantilla HTML"):
    st.code("""
<!DOCTYPE html>
<html>
<head>
  <title>Documento Ejemplo</title>
</head>
<body>
  <h1>Hola {{nombre}}</h1>
  <p>Email: {{email}}</p>
  <p>Teléfono: {{telefono}}</p>
  <p>{{mensaje}}</p>
</body>
</html>
""", language="html")

# Procesamiento de plantilla
if template_file:
    template = template_file.read().decode('utf-8')
    st.success("✅ Plantilla cargada correctamente")
    
    # Opción para ver vista previa
    if st.checkbox("👁️ Ver vista previa de la plantilla original"):
        st.info("Vista previa de cómo se ve tu plantilla con los placeholders aún sin reemplazar:")
        st.components.v1.html(template, height=500, scrolling=True)
        st.divider()

    # Extraer placeholders
    placeholders = extraer_placeholders(template)

    if not placeholders:
        st.warning("⚠️ No se encontraron placeholders en la plantilla (usa el formato {{nombre}}).")
    else:
        st.subheader("2. Completa los campos detectados en la plantilla")

        # Formulario dinámico
        with st.form("formulario_html"):
            datos = {}

            for ph in placeholders:
                # Clasificar posibles campos largos en text_area
                descripcion = PLACEHOLDER_INFO.get(ph, None)
                if ph.lower() in ["mensaje", "descripcion", "texto", "contenido"]:
                    datos[ph] = st.text_area(
                        ph.capitalize(),
                        placeholder=f"Introduce el valor para {ph}...",
                        help=descripcion,
                        height=120
                    )
                else:
                    datos[ph] = st.text_input(
                        ph.capitalize(),
                        placeholder=f"Introduce el valor para {ph}...",
                        help=descripcion
                    )

            st.divider()
            submitted = st.form_submit_button("🚀 Generar HTML", use_container_width=True, type="primary")

        if submitted:
            html_final = rellenar_plantilla(template, datos)

            st.success("✅ HTML generado exitosamente")
            st.divider()

            tab1, tab2 = st.tabs(["👁️ Vista Previa", "📝 Código HTML"])
            with tab1:
                st.components.v1.html(html_final, height=500, scrolling=True)
            with tab2:
                st.code(html_final, language='html')

            st.divider()
            st.download_button(
                label="⬇️ Descargar HTML",
                data=html_final,
                file_name="documento_generado.html",
                mime="text/html",
                use_container_width=True
            )

st.divider()
st.caption("Hecho con Streamlit")