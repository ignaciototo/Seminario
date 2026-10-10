# 📦 Asistente WMS — Triaje Inteligente de Consultas Operativas

## Trabajo Práctico Integrador: Del Problema al Deploy

* **Carrera:** Tecnicatura Superior en Ciencia de Datos e IA — IFTS N.° 18  
* **Materia:** Seminario de Actualización (Año 2026 — 2° Cuatrimestre)  
* **Docente:** Cynthia M. Villagra  
* **Alumno:** Toto Ignacio  
* **Fecha:** 16 de Octubre de 2026  

---

## 🎯 1. El Problema de Negocio

En el marco de la migración de un sistema de gestión de depósitos (**WMS**) desarrollado internamente hace 20 años hacia un software estándar de mercado, los operarios de almacén se enfrentan a un cambio abrupto de flujos y pantallas.

Durante las primeras semanas posteriores a la implementación productiva:

* Los **Key Users** se ven saturados respondiendo dudas operativas básicas.
* Los operarios dispersan las consultas enviando la misma pregunta a a través de múltiples canales (WhatsApp, Teams, radio) generando demoras y desorganización.

Se busca reducir esta carga de trabajo con un asistente virtual que pueda orientar o derivar las consultas únicamente al canal y personas adecuadas.

### ¿Por qué un modelo de NLP (Zero-Shot) y no reglas `if/else`?

El depósito maneja un vocabulario técnico y dinámico:

1. **Jerga especializada y siglas:** *PDA, PLU, HDR (Hoja de Ruta), Hueco, Slotting, Bultos, Pallets, Retrabajo*.
2. **Spanglish:** *Pickear, piking, packing*.
3. **Fallas de las reglas sintácticas:** Palabras como *"PDA"* o *"Pallets"* aparecen en casi todas las frases. Un sistema basado en `if "pda" in texto` es incapaz de discernir si la consulta corresponde a *Picking*, *Recepción*, *Expedición* o *Control de Inventario*.

La solución implementa **Zero-Shot Classification con NLI**, permitiendo clasificar preguntas en lenguaje natural y sugerir el área y referente exacto sin requerir entrenamiento previo.

---

## 🧠 2. Arquitectura y Modelos Evaluados

En la notebook de experimentación ([`TPI_Toto_Ignacio.ipynb`](TPI_Toto_Ignacio.ipynb)) se compararon dos modelos del Hub de Hugging Face:

| Métrica / Característica | BERT-XNLI (`Recognai/bert-base-spanish-wwm-cased-xnli`) | SELECTRA-Medium (`Recognai/zeroshot_selectra_medium`) |
| --- | --- | --- |
| **Arquitectura** | BERT Base (110M parámetros) | ELECTRA Medium (38M parámetros) |
| **Tamaño de pesos** | ~440 MB | **~163 MB (63% más liviano)** |
| **Tiempo de carga en frío** | ~6.58 s | **~0.72 s (9.1x más rápido)** |
| **Latencia promedio por inferencia** | ~0.82 s | **~0.22 s (3.7x más veloz)** |
| **Consumo de memoria RAM** | ~600 MB - 800 MB | **< 300 MB (Apto Free Tier de 1 GB)** |

### Decisión para el Deploy

Se seleccionó **`Recognai/zeroshot_selectra_medium`** para la aplicación web por su tamaño y velocidad de respuesta, para evitar que el contenedor en **Streamlit Community Cloud** no supere el límite estricto de **1 GB de RAM**.

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

> ℹ️ **Nota:** La aplicación (`app.py`), el notebook y las pruebas locales **no requieren token de HF**. Para ejecutar `probar_inference_client.py` para probar la API serverless de Hugging Face, renombra `.env.example` a `.env` e ingresa tu token que puedes generar en **<https://huggingface.co/settings/tokens>**.

---

## 📂 4. Estructura del Proyecto

```text
TOTO_IGNACIO_TPI/
├── app.py                      # Aplicación web interactiva en Streamlit
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación completa y guía de uso
├── .env.example                # Plantilla de variables de entorno (optativo para API)
├── TPI_Toto_Ignacio.ipynb      # Notebook Jupyter con el benchmark y análisis
├── comparativa_modelos.csv     # Resultados experimentales de ambos modelos
├── probar_local.py             # Script de validación local del benchmark
└── probar_inference_client.py  # Script de prueba de la API de Hugging Face
```

---

## 🌐 5. Deploy en la Nube (Streamlit Community Cloud)

* **Enlace a la Aplicación en Vivo:** `https://seminario.streamlit.app/`
* **Enlace al Repositorio en GitHub:** `https://github.com/ignaciototo/Seminario/tree/main/TOTO_IGNACIO_TPI`

---

## 🎓 6. Autor

* **Toto Ignacio** — Tecnicatura Superior en Ciencia de Datos e IA (IFTS N.° 18).
