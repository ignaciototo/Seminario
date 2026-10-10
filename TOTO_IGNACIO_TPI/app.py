import os
import time
import pandas as pd
import streamlit as st

from PIL import Image
try:
    logo_img = Image.open("logo.png")
except FileNotFoundError:
    logo_img = "📦"

# -----------------------------------------------------------------------------
# 1. Configuración de la Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asistente WMS — Gestión Inteligente",
    page_icon=logo_img,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Clase Clasificadora (Objeto del Negocio WMS)
# -----------------------------------------------------------------------------
class WmsClassifierService:
    """Gestión de dudas operativas del WMS."""

    def __init__(self, model_name: str = "Recognai/zeroshot_selectra_medium") -> None:
        from transformers import pipeline
        
        self.model_name: str = model_name
        self.classifier = pipeline(
            task="zero-shot-classification",
            model=self.model_name,
            device=-1
        )

    def classify_ticket(self, query_text: str, candidate_areas: list[str]) -> dict:
        """Clasifica una consulta y retorna probabilidades ordenadas."""
        hypothesis: str = "Esta consulta corresponde al área de {}."
        prediction_result = self.classifier(
            query_text,
            candidate_labels=candidate_areas,
            hypothesis_template=hypothesis
        )
        return prediction_result


# -----------------------------------------------------------------------------
# 3. Cache del Modelo
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Iniciando modelo NLP liviano (SELECTRA Medium)...")
def load_classifier_service() -> WmsClassifierService:
    """Instancia y cachea el servicio de clasificación en memoria."""
    return WmsClassifierService(model_name="Recognai/zeroshot_selectra_medium")


# -----------------------------------------------------------------------------
# 4. Datos Maestros de Áreas y Referentes Operativos
# -----------------------------------------------------------------------------
DEFAULT_AREAS = [
    "Recepción de Pallets",
    "Preparación de Pedidos",
    "Almacenamiento de pallets",
    "Expedición de Camiones",
    "Despacho de pedidos",
    "Planificación de viajes",
    "Control de Inventario",
    "Sistemas y Soporte WMS"
]

CONTACT_DIRECTORY = {
    "Recepción de Pallets": {
        "referente": "Jefe de Recepción / Key User Recepción",
        "canal": "#soporte-recepcion-wms"
    },
    "Preparación de Pedidos": {
        "referente": "Supervisor de Preparación / Key User Picking",
        "canal": "#soporte-picking-wms"
    },
    "Almacenamiento de pallets": {
        "referente": "Responsable de Slotting y Guardado",
        "canal": "#soporte-guardado-wms"
    },
    "Expedición de Camiones": {
        "referente": "Coordinador de Dársenas / Key User Despacho",
        "canal": "#soporte-expedicion-wms"
     },
    "Despacho de pedidos": {
        "referente": "Coordinador de Despacho",
        "canal": "#soporte-despacho-wms"
    },
    "Planificación de viajes": {
        "referente": "Planificación Logística",
        "canal": "#mesa-planeamiento-wms"
    },
    "Control de Inventario": {
        "referente": "Auditor de Stock",
        "canal": "#mesa-inventarios-wms"
    },
    "Sistemas y Soporte WMS": {
        "referente": "Mesa de Ayuda TI",
        "canal": "#soporte-tecnico-wms"
    }
}

EJEMPLOS_WMS = [
    "— Seleccionar un ejemplo operativo del depósito —",
    "Estoy recepcionando un pale que tiene rotura. Como lo registro?",
    "Los pallets que estamos descargando en la rece están fuera de estandar. Tengo que cobrar el retrabajo al proveedor. Que función de la PDA era?",
    "El plan quedó chico. Necesito que envien más volumen para replnificar. Sino van a quedar los camiones por la mitad.",
    "Terminé de descargar y la PDA me manda a guardar el pallet en el pasillo 14, pero la altura del hueco no da para este bulto. Como pido reubicarlo?",
    "En el Hueco no está el PLU que me dice la PDA que tengo que pickear. Como registro la incidencia?",
    "La repo de mercadería me envío a reponer a un hueco de picking que está lleno.",
    "Que función de la PDA es la que tengo que acceder para consolidar pallets pa subir al camión?",
    "El camión está lleno pero la HDR tiene más pallets.",
    "Estoy en el andén. Me falta cerrar el camión para que salga a la calle. Pero no se como se hace.",
    "En el controlde rutina, detectamos diferencias entre el stock físico y lo que dice el wms. Me faltan 3 bultos del PLU 42222 en el rack",
    "La PDA quiere consolidar pales de pollo con veneno para subirlos a un camión. Eso está mal.",
    "La PDA está tirando error de conexión al WIFI."
]

# -----------------------------------------------------------------------------
# 5. Interfaz de Usuario (Streamlit)
# -----------------------------------------------------------------------------
def main() -> None:
    # Sidebar
    with st.sidebar:

        st.subheader("⚙️ Modelo en Ejecución")
        st.success("🤖 **SELECTRA-Medium**\n\n*Zero-Shot NLI en Español*")

        st.divider()
        st.subheader("🏷️ Áreas Operativas Configuradas")
        areas_activas = st.multiselect(
            "Podés agregar o quitar áreas:",
            options=DEFAULT_AREAS,
            default=DEFAULT_AREAS
        )

        st.divider()
        st.info("💡 Usá el selector de ejemplos de consultas, o ingresa consultas manualmente.")

    col_logo, col_title = st.columns([1, 6], vertical_alignment="center")
    with col_logo:
        if isinstance(logo_img, str):
            st.title("📦")
        else:
            st.image(logo_img, use_container_width=True)
    with col_title:
        st.title("Asistente de Mesa de Ayuda WMS")
        st.markdown(
            "##### Gestión y derivación automática de dudas operativas"
        )

    st.subheader("1. Ingreso de la Consulta Operativa")

    ejemplo_seleccionado = st.selectbox(
        "Cargar consulta de prueba predefinida:",
        options=EJEMPLOS_WMS,
        index=0
    )

    texto_inicial = "" if ejemplo_seleccionado.startswith("—") else ejemplo_seleccionado

    consulta_usuario = st.text_area(
        "Describí la duda o incidencia del depósito:",
        value=texto_inicial,
        placeholder="Ejemplo: La colectora me pide pickear del hueco A-12 pero la posición está vacía...",
        height=120
    )

    btn_clasificar = st.button("🚀 Analizar Consulta y Derivar", type="primary", use_container_width=True)

    # Ejecución de la Clasificación
    if btn_clasificar:
        if not consulta_usuario.strip():
            st.warning("⚠️ Por favor ingresá una consulta o seleccioná un ejemplo de la lista.")
            return

        if len(areas_activas) < 2:
            st.error("⚠️ Debés seleccionar al menos 2 áreas operativas en la barra lateral para comparar.")
            return

        with st.status("🧠 Procesando consulta...", expanded=True) as status:
            st.write("Cargando modelo en memoria y tokenizando texto...")
            classifier_service = load_classifier_service()
            time.sleep(0.4)
            st.write("Analizando intenciones y contextos operativos...")
            
            t_inicio = time.time()
            resultado = classifier_service.classify_ticket(consulta_usuario, areas_activas)
            latencia = time.time() - t_inicio
            
            time.sleep(0.4)
            status.update(label="Análisis finalizado", state="complete", expanded=False)

        # Procesamiento de resultados
        etiquetas = resultado["labels"]
        probabilidades = resultado["scores"]

        area_ganadora = etiquetas[0]
        confianza_ganadora = probabilidades[0] * 100

        segunda_area = etiquetas[1]
        segunda_confianza = probabilidades[1] * 100

        st.divider()
        st.subheader("2. Derivación Sugerida")

        # Tarjeta principal con recomendación de derivación
        info_area = CONTACT_DIRECTORY.get(area_ganadora, {
            "referente": "Key User de Área",
            "canal": "#soporte-general-wms"
        })

        res_col1, res_col2 = st.columns([1.5, 1])

        with res_col1:
            st.success(f"🎯 **Área:** {area_ganadora} ({confianza_ganadora:.1f}%)")
            st.markdown(f"**Segunda opción:** {segunda_area} ({segunda_confianza:.1f}%)")
            st.divider()
            st.markdown(f"**👤 Referente Asignado:** {info_area['referente']}")
            st.markdown(f"**💬 Canal de Contacto (Teams/Discord):** `{info_area['canal']}`")
            st.caption(f"⚡ Inferencia resuelta en **{latencia*1000:.0f} ms**.")

        with res_col2:
            st.markdown("#### Distribución de Probabilidades")
            df_chart = pd.DataFrame({
                "Área": etiquetas,
                "Probabilidad (%)": [p * 100 for p in probabilidades]
            })

            import altair as alt
            bars = alt.Chart(df_chart).mark_bar(color='#2563EB', cornerRadiusEnd=4).encode(
                x=alt.X('Probabilidad (%):Q', title='Probabilidad (%)', axis=alt.Axis(format='.0f')),
                y=alt.Y('Área:N', sort='-x', title=None),
                tooltip=[alt.Tooltip('Área:N'), alt.Tooltip('Probabilidad (%):Q', format='.2f')]
            )
            text = bars.mark_text(
                align='left',
                baseline='middle',
                dx=3  # Nudges text to right
            ).encode(
                text=alt.Text('Probabilidad (%):Q', format='.2f')
            )
            chart = (bars + text).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
