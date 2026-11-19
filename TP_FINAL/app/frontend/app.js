// CardioCheck AI - Frontend Logic
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictionForm");
  const apiUrlInput = document.getElementById("apiUrlInput");
  const btnTestApi = document.getElementById("btnTestApi");
  const apiStatusBadge = document.getElementById("apiStatusBadge");
  const apiStatusText = document.getElementById("apiStatusText");

  const btnPresetHealthy = document.getElementById("btnPresetHealthy");
  const btnPresetRisk = document.getElementById("btnPresetRisk");

  const btnSubmit = document.getElementById("btnSubmit");
  const btnText = document.getElementById("btnText");
  const spinner = document.getElementById("spinner");

  const initialState = document.getElementById("initialState");
  const errorAlert = document.getElementById("errorAlert");
  const errorTitle = document.getElementById("errorTitle");
  const errorMessage = document.getElementById("errorMessage");

  const resultBox = document.getElementById("resultBox");
  const riskBadge = document.getElementById("riskBadge");
  const probValue = document.getElementById("probValue");
  const progressBar = document.getElementById("progressBar");
  const resultDiagnosis = document.getElementById("resultDiagnosis");
  const adviceText = document.getElementById("adviceText");
  const jsonResponse = document.getElementById("jsonResponse");

  // Helper para obtener URL base limpia
  function getBaseApiUrl() {
    return apiUrlInput.value.trim().replace(/\/+$/, "");
  }

  // 1. Comprobar estado de la API (GET /health)
  async function checkApiHealth() {
    const baseUrl = getBaseApiUrl();
    apiStatusBadge.className = "api-status-badge";
    apiStatusText.textContent = "Comprobando...";

    try {
      const response = await fetch(`${baseUrl}/health`, {
        method: "GET",
        headers: { "Accept": "application/json" }
      });

      if (response.ok) {
        const data = await response.json();
        apiStatusBadge.classList.add("online");
        apiStatusText.textContent = `Online (${data.estado || "ok"})`;
        hideError();
      } else {
        apiStatusBadge.classList.add("offline");
        apiStatusText.textContent = `HTTP ${response.status}`;
      }
    } catch (err) {
      apiStatusBadge.classList.add("offline");
      apiStatusText.textContent = "Offline / Sin conexión";
    }
  }

  // 2. Presets de prueba rápida (Ideales para la demo en vivo de 5 minutos)
  btnPresetHealthy.addEventListener("click", () => {
    document.getElementById("age").value = 35;
    document.getElementById("sex").value = "0"; // Femenino
    document.getElementById("chest").value = "2"; // Angina atípica
    document.getElementById("resting_blood_pressure").value = 115;
    document.getElementById("serum_cholestoral").value = 180;
    document.getElementById("maximum_heart_rate_achieved").value = 175;
    document.getElementById("exercise_induced_angina").value = "0"; // No
  });

  btnPresetRisk.addEventListener("click", () => {
    document.getElementById("age").value = 65;
    document.getElementById("sex").value = "1"; // Masculino
    document.getElementById("chest").value = "4"; // Asintomático (patológico)
    document.getElementById("resting_blood_pressure").value = 160;
    document.getElementById("serum_cholestoral").value = 286;
    document.getElementById("maximum_heart_rate_achieved").value = 108;
    document.getElementById("exercise_induced_angina").value = "1"; // Sí
  });

  btnTestApi.addEventListener("click", checkApiHealth);

  // 3. Manejo de Errores UI
  function showError(title, message) {
    errorTitle.textContent = title;
    errorMessage.textContent = message;
    errorAlert.classList.remove("hidden");
    resultBox.classList.add("hidden");
    initialState.classList.add("hidden");
  }

  function hideError() {
    errorAlert.classList.add("hidden");
  }

  // 4. Envío del Formulario (POST /predecir)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    // Construcción del payload según el contrato de la API
    const payload = {
      age: parseInt(document.getElementById("age").value, 10),
      sex: parseInt(document.getElementById("sex").value, 10),
      chest: parseInt(document.getElementById("chest").value, 10),
      resting_blood_pressure: parseFloat(document.getElementById("resting_blood_pressure").value),
      serum_cholestoral: parseFloat(document.getElementById("serum_cholestoral").value),
      maximum_heart_rate_achieved: parseFloat(document.getElementById("maximum_heart_rate_achieved").value),
      exercise_induced_angina: parseInt(document.getElementById("exercise_induced_angina").value, 10)
    };

    // Estado de carga
    btnSubmit.disabled = true;
    btnText.textContent = "Procesando...";
    spinner.classList.remove("hidden");

    const baseUrl = getBaseApiUrl();

    try {
      const response = await fetch(`${baseUrl}/predecir`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Manejo de Error 422 (Validación Pydantic)
      if (response.status === 422) {
        const errorData = await response.json();
        const detailMsg = errorData.detail 
          ? JSON.stringify(errorData.detail, null, 2)
          : "Datos de entrada inválidos o tipos de datos incorrectos.";
        showError("Error 422: Validación de Entrada", `El backend rechazó los datos: ${detailMsg}`);
        return;
      }

      // Manejo de Error 500 u otros errores del servidor
      if (!response.ok) {
        showError(`Error ${response.status}`, `El servidor respondió con código ${response.status}.`);
        return;
      }

      // Éxito 200 OK
      const data = await response.json();
      renderResult(data);

    } catch (err) {
      console.error("Fetch error:", err);
      showError(
        "Fallo de Conexión (API Inaccesible)",
        "No se pudo conectar con el backend. Si está alojado en Render gratuito, puede estar 'despertando' tras inactividad (tarda 30-50 segundos). Verificá también la URL y la configuración de CORS."
      );
    } finally {
      btnSubmit.disabled = false;
      btnText.textContent = "Realizar Predicción";
      spinner.classList.add("hidden");
    }
  });

  // 5. Renderizado de resultados
  function renderResult(data) {
    initialState.classList.add("hidden");
    resultBox.classList.remove("hidden");

    // data.prediccion (0 o 1) y data.probabilidad (0.0 a 1.0)
    const pred = data.prediccion;
    const prob = typeof data.probabilidad === "number" ? data.probabilidad : 0.5;
    const probPercent = (prob * 100).toFixed(1);

    probValue.textContent = `${probPercent}%`;
    progressBar.style.width = `${probPercent}%`;

    if (pred === 1 || prob >= 0.5) {
      // Alto riesgo
      riskBadge.textContent = "RIESGO CARDÍACO DETECTADO";
      riskBadge.className = "badge high-risk";
      progressBar.className = "progress-bar-fill high";
      resultDiagnosis.textContent = "El modelo detecta patrones compatibles con riesgo o presencia de cardiopatía coronaria.";
      adviceBox.style.borderLeftColor = "var(--danger)";
      adviceText.textContent = "Se sugiere interconsulta con cardiología para realizar estudios complementarios (ecocardiograma, ergometría).";
    } else {
      // Bajo riesgo
      riskBadge.textContent = "BAJO RIESGO CARDÍACO";
      riskBadge.className = "badge low-risk";
      progressBar.className = "progress-bar-fill low";
      resultDiagnosis.textContent = "Los parámetros ingresados se encuentran dentro de los rangos estadísticos normales de baja probabilidad de riesgo.";
      adviceBox.style.borderLeftColor = "var(--success)";
      adviceText.textContent = "Mantener hábitos de vida saludable, control anual de presión arterial y chequeo lipídico preventivo.";
    }

    jsonResponse.textContent = JSON.stringify(data, null, 2);
  }

  // Comprobar estado al cargar la página
  checkApiHealth();
});
