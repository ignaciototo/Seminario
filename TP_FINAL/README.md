# 🫀 CardioCheck AI - Predicción de Riesgo Cardiovascular

Sistema integral de predicción de riesgo coronario ambulatorio mediante **Machine Learning**, desarrollado con **FastAPI** en el backend y una interfaz web moderna en el frontend.

Proyecto final desarrollado para la **Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial** — **IFTS N.º 18** (Seminario de Actualización).

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Variables Clínicas (Features)](#-variables-clínicas-features)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Ejecución Local](#-instalación-y-ejecución-local)
  - [1. Clonar o Descargar el Proyecto](#1-clonar-o-descargar-el-proyecto)
  - [2. Configurar el Entorno Virtual](#2-configurar-el-entorno-virtual)
  - [3. Instalar Dependencias](#3-instalar-dependencias)
  - [4. Iniciar el Backend (API FastAPI)](#4-iniciar-el-backend-api-fastapi)
  - [5. Ejecutar el Frontend](#5-ejecutar-el-frontend)
- [Uso de la Aplicación Web](#-uso-de-la-aplicación-web)
- [Documentación de la API (Endpoints)](#-documentación-de-la-api-endpoints)
- [Entrenamiento del Modelo (Notebook)](#-entrenamiento-del-modelo-notebook)
- [Despliegue en Producción (Cloud)](#-despliegue-en-producción-cloud)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Créditos e Información Académica](#-créditos-e-información-académica)

---

## 📖 Descripción General

**CardioCheck AI** permite estimar la probabilidad de que un paciente presente patologías cardíacas coronarias a partir de 7 variables clínicas accesibles en una consulta ambulatoria de rutina. 

El sistema consta de:
1. **Modelo Predictivo:** Pipeline de scikit-learn con preprocesamiento y **Regresión Logística**, entrenado sobre el dataset internacional *Heart Statlog* (OpenML ID 53 / UCI ML Repository).
2. **Backend API:** Servicio RESTful desarrollado en **FastAPI**, validado con **Pydantic** y servido con **Uvicorn**, capaz de realizar inferencias en tiempo real y devolver la probabilidad estimada junto a un diagnóstico orientativo.
3. **Frontend Web:** Aplicación web responsiva (HTML5, CSS3, JavaScript Vanilla) con selector dinámico de backend, presets rápidos de prueba, indicador de estado de conexión (`/health`) y recomendaciones médicas preventivas.

---

## 📂 Estructura del Proyecto

```text
TP_FINAL/
├── app/
│   ├── backend/
│   │   ├── main.py              # API FastAPI y definición de endpoints
│   │   └── requirements.txt     # Dependencias de Python para el backend
│   ├── frontend/
│   │   ├── index.html           # Interfaz de usuario (formulario y resultados)
│   │   ├── styles.css           # Estilos visuales y diseño responsivo
│   │   ├── app.js               # Lógica del cliente, llamadas fetch y validaciones
│   │   ├── logo.svg             # Isologotipo de CardioCheck
│   │   └── ifts18_logo.jpg      # Logo institucional IFTS N.º 18
│   └── modelo/
│       └── modelo.joblib        # Modelo entrenado exportado con joblib
├── notebook/
│   └── entrenamiento.ipynb      # EDA, experimentación, entrenamiento y evaluación
├── Consigna.pdf                 # Requisitos y consigna académica del trabajo
├── ifts18_logo.jpg              # Logo institucional
└── README.md                    # Esta guía de uso e implementación
```

---

## 🩺 Variables Clínicas (Features)

Para maximizar la aplicabilidad en atención médica primaria, se seleccionaron **7 variables no invasivas**:

| Variable | Nombre en API | Tipo | Rango / Valores permitidos | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| **Edad** | `age` | Entero | `18 - 120` años | Edad cronológica del paciente |
| **Sexo** | `sex` | Entero | `1` o `0` | `1` = Masculino, `0` = Femenino |
| **Dolor de Pecho** | `chest` | Entero | `1 - 4` | `1`: Angina típica, `2`: Angina atípica, `3`: No anginoso, `4`: Asintomático |
| **Presión Arterial** | `resting_blood_pressure` | Decimal | `50 - 250` mm Hg | Presión sistólica en reposo al ingresar a consulta |
| **Colesterol** | `serum_cholestoral` | Decimal | `80 - 700` mg/dl | Colesterol sérico total en sangre |
| **Frec. Cardíaca Máx.** | `maximum_heart_rate_achieved` | Decimal | `50 - 250` lpm | Frecuencia cardíaca máxima alcanzada en esfuerzo |
| **Angina por Ejercicio** | `exercise_induced_angina` | Entero | `1` o `0` | `1` = Sí presenta dolor inducido por esfuerzo, `0` = No |

---

## ⚙️ Requisitos Previos

- **Python:** Versión `3.10`, `3.11`, `3.12` o `3.13`.
- **Navegador Web:** Chrome, Edge, Firefox, Safari o similar.
- **Git** (opcional, para clonar el repositorio).

---

## 🚀 Instalación y Ejecución Local

### 1. Clonar o Descargar el Proyecto

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TP_FINAL
```

*(Si lo descargaste en un archivo ZIP, descomprimílo y abrí una terminal en la carpeta raíz del proyecto).*

---

### 2. Configurar el Entorno Virtual

Es recomendable crear un entorno virtual aislado para no alterar las librerías globales:

**En Windows (PowerShell / CMD):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar Dependencias

Instalá los paquetes necesarios para ejecutar la API y el modelo:

```bash
pip install -r app/backend/requirements.txt
```

*(Las dependencias principales son: `fastapi`, `uvicorn`, `pydantic`, `scikit-learn`, `joblib`, `pandas` y `numpy`).*

---

### 4. Iniciar el Backend (API FastAPI)

Desde la raíz del proyecto (`TP_FINAL`), ejecutá Uvicorn:

```bash
uvicorn app.backend.main:app --reload --port 8000
```

> **Verificación:**  
> - La consola indicará: `Application startup complete. Uvicorn running on http://127.0.0.1:8000`
> - Podés ingresar a tu navegador en [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) para ver: `{"estado": "ok"}`
> - La documentación interactiva Swagger se encuentra en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 5. Ejecutar el Frontend

Podés abrir la interfaz de dos maneras:

#### Opción A: Servidor HTTP local (Recomendada)
Para evitar bloqueos de políticas CORS en navegadores estrictos, iniciá un servidor estático rápido:

```bash
# En una nueva terminal, parate en la carpeta app/frontend
cd app/frontend
python -m http.server 3000
```
Luego abrí en tu navegador: **[http://localhost:3000](http://localhost:3000)**

#### Opción B: Apertura directa del archivo
Simplemente hacé doble clic sobre el archivo `app/frontend/index.html` o abrilo con cualquier navegador web.

> 💡 **Importante si ejecutás en local:**  
> En la barra superior de la web, asegurate de que la **URL del Backend** apunte a `http://127.0.0.1:8000` y hacé clic en **Test** para comprobar que el indicador cambie a **Online (ok)**.

---

## 🖥️ Uso de la Aplicación Web

1. **Verificar Conexión:** En el encabezado superior observarás el estado de la API (`Online` en verde si está conectada).
2. **Carga Rápida (Presets):**
   - Hacé clic en **"💡 Cargar Sano"** para rellenar automáticamente el formulario con valores representativos de bajo riesgo.
   - Hacé clic en **"⚠️ Cargar Riesgo"** para evaluar un caso clínico con signos de alerta.
3. **Ingreso Manual:** Modificá o ingresá los valores clínicos del paciente.
4. **Realizar Predicción:** Presioná el botón principal. La aplicación mostrará:
   - Indicador visual (**BAJO RIESGO** en verde o **ALTO RIESGO CARDÍACO** en rojo).
   - Barra de progreso con la probabilidad porcentual exacta.
   - Recomendaciones médicas y preventivas personalizadas.
   - Detalle técnico desplegable con el JSON devuelto por la API.

---

## 📡 Documentación de la API (Endpoints)

### `GET /health`
Comprueba la disponibilidad del servicio.

- **Respuesta (`200 OK`):**
  ```json
  {
    "estado": "ok"
  }
  ```

---

### `POST /predecir`
Recibe los datos del paciente y devuelve la inferencia del modelo.

- **Ejemplo de Solicitud (Request Body):**
  ```json
  {
    "age": 58,
    "sex": 1,
    "chest": 4,
    "resting_blood_pressure": 150.0,
    "serum_cholestoral": 270.0,
    "maximum_heart_rate_achieved": 115.0,
    "exercise_induced_angina": 1
  }
  ```

- **Ejemplo de Respuesta (`200 OK`):**
  ```json
  {
    "prediccion": 1,
    "probabilidad": 0.8412,
    "diagnostico": "Riesgo cardíaco detectado"
  }
  ```

---

## 🔬 Entrenamiento del Modelo (Notebook)

El proceso completo de análisis exploratorio, ingeniería de datos, experimentación y validación se encuentra en `notebook/entrenamiento.ipynb`:

1. **Dataset:** Statlog Heart (OpenML ID 53), 270 pacientes sin valores nulos.
2. **Estrategia de Partición:** 80% entrenamiento / 20% prueba con partición estratificada (`stratify=y`).
3. **Modelos comparados:** Regresión Logística, Random Forest y K-Nearest Neighbors evaluados con validación cruzada enfocada en métricas de **Recall (Sensibilidad)** y **ROC-AUC** para minimizar falsos negativos en el ámbito de la salud.
4. **Resultados del Modelo Final (Regresión Logística):**
   - **Accuracy en Test:** ~77.8%
   - **ROC-AUC:** > 0.82
5. **Persistencia:** Guardado mediante `joblib.dump` en `app/modelo/modelo.joblib`.

Para reproducirlo:
```bash
pip install jupyter notebook matplotlib seaborn
jupyter notebook notebook/entrenamiento.ipynb
```

---

## ☁️ Despliegue en Producción (Cloud)

### Despliegue del Backend (por ejemplo en Render / Railway)

1. Crear un nuevo servicio web (**Web Service**) conectado al repositorio de GitHub.
2. Configurar los parámetros de compilación y ejecución:
   - **Root Directory:** *(dejar en blanco o seleccionar raíz)*
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r app/backend/requirements.txt`
   - **Start Command:** `uvicorn app.backend.main:app --host 0.0.0.0 --port $PORT`
3. Copiar la URL pública asignada (ejemplo: `https://cardiocheck-kila.onrender.com`).

### Despliegue del Frontend (Vercel, GitHub Pages, Netlify o Render)

1. Alojar los archivos estáticos de la carpeta `app/frontend/`.
2. En `app/frontend/index.html` (o directamente desde la barra de configuración en la web), configurar el valor predeterminado del input `apiUrlInput` con la URL HTTPS de tu backend en producción.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.13 / 3.10+
- **Machine Learning & Datos:** `scikit-learn`, `pandas`, `numpy`, `joblib`
- **Framework Web Backend:** `FastAPI`, `uvicorn`, `pydantic`
- **Frontend:** HTML5 semántico, CSS3 moderno (Variables CSS, Flexbox/Grid, Animaciones), JavaScript Vanilla (Fetch API asíncrona)
- **Visualización & Notebooks:** Jupyter Notebook, Matplotlib, Seaborn

---

## 🎓 Créditos e Información Académica

- **Institución:** Instituto de Formación Técnica Superior N.º 18 (IFTS 18) - GCBA
- **Carrera:** Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial
- **Materia:** Seminario de Actualización
- **Docente:** Prof. Cynthia Villagra
- **Ciclo Lectivo:** 2026 - 2.º Cuatrimestre
