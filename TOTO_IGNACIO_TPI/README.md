# 📦 Asistente WMS — Triaje Inteligente de Consultas Operativas

## Trabajo Práctico Integrador: Del Problema al Deploy

* **Carrera:** Tecnicatura Superior en Ciencia de Datos e IA — IFTS N.° 18  
* **Materia:** Seminario de Actualización (Ciclo Lectivo 2026 — 2.° Cuatrimestre)  
* **Docente:** Cynthia M. Villagra  
* **Alumno:** Toto Ignacio  
* **Fecha:** Octubre 2026  

---

## 🎯 1. El Problema de Negocio

En el marco de la migración de un sistema de gestión de depósitos (**WMS**) desarrollado internamente hace 20 años hacia un software estándar de mercado, los operarios de almacén se enfrentan a un cambio abrupto de flujos y pantallas.

Durante las primeras semanas de arranque en vivo (*Go-Live*):

* Los usuarios clave (**Key Users**) quedan saturados respondiendo dudas operativas básicas.
* Los operarios dispersan las consultas enviando la misma pregunta a múltiples grupos de chat (WhatsApp, Teams, radio) generando demoras y desorganización.

### ¿Por qué un modelo de NLP (Zero-Shot) y no reglas `if/else`?

El depósito maneja un vocabulario técnico y dinámico:

1. **Jerga especializada y siglas:** *PDA, PLU, HDR (Hoja de Ruta), Hueco, Slotting, Bultos, Pallets, Retrabajo*.
2. **Spanglish logístico:** *Pickear, piking, reapro, consolidar, andén*.
3. **Fallas de las reglas sintácticas:** Palabras como *"PDA"* o *"Pallets"* aparecen en casi todas las frases. Un sistema basado en `if "pda" in texto` es incapaz de discernir si la consulta corresponde a *Picking*, *Recepción*, *Expedición* o *Control de Inventario*.

La solución implementa **Zero-Shot Classification con NLI**, permitiendo clasificar preguntas en lenguaje natural y sugerir el área y referente exacto sin requerir entrenamiento previo.

---

## 🧠 2. Arquitectura y Modelos Evaluados

En la notebook de experimentación ([`TPI_Toto_Ignacio.ipynb`](TPI_Toto_Ignacio.ipynb)) se compararon dos modelos del Hub de Hugging Face:

| Métrica / Característica | BERT-XNLI (`Recognai/bert-base-spanish-wwm-cased-xnli`) | SELECTRA-Medium (`Recognai/zeroshot_selectra_medium`) |
| --- | --- | --- |
| **Arquitectura** | BERT Base (110M parámetros) | ELECTRA Medium (38M parámetros) |
| **Tamaño de pesos** | ~440 MB | **~163 MB** |
| **Tiempo de carga en memoria** | 6.15 s | **0.64 s (9.6x más rápido)** |
| **Latencia promedio por inferencia** | ~0.42 s | **~0.18 s (2.3x más veloz)** |
| **Consumo de memoria RAM** | ~600 MB - 800 MB | **< 300 MB (Apto Free Tier)** |

### Decisión para el Deploy

Se seleccionó **`Recognai/zeroshot_selectra_medium`** para la aplicación web por su extrema ligereza y velocidad de respuesta, garantizando que el contenedor en **Streamlit Community Cloud** no supere el límite estricto de **1 GB de RAM**.

---

## 💻 3. Cómo Ejecutar la Aplicación Localmente

### Paso 1: Clonar el repositorio

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd TOTO_IGNACIO_TPI
```

### Paso 2: Crear y activar entorno virtual

```bash
# En Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1

# En Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Iniciar la app de Streamlit

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en:  
👉 **`http://localhost:8501`**

---

## 📂 4. Estructura de Archivos del Proyecto

```text
TOTO_IGNACIO_TPI/
├── app.py                      # Aplicación web interactiva en Streamlit
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación completa y guía de uso
├── TPI_Toto_Ignacio.ipynb      # Notebook Jupyter con el benchmark y análisis
├── comparativa_modelos.csv     # Resultados experimentales de ambos modelos
├── flujo.drawio                # Diagrama de arquitectura del sistema
├── probar_local.py             # Script de validación local del benchmark
├── probar_inference_client.py  # Script de prueba de la API de Hugging Face
├── Trabajo Práctico Integrador.docx # Informe del trabajo para la entrega
└── Presentacion_TPI_Toto_Ignacio.pptx # Presentación ejecutiva para la defensa
```

---

## 🌐 5. Deploy en la Nube (Streamlit Community Cloud)

* **Enlace a la Aplicación en Vivo:** `[AGREGAR LINK DE STREAMLIT CLOUD]`
* **Enlace al Repositorio en GitHub:** `[AGREGAR LINK DE GITHUB]`

---

## 🎓 6. Autor

* **Toto Ignacio** — Alumno de la Tecnicatura Superior en Ciencia de Datos e IA (IFTS N.° 18).
