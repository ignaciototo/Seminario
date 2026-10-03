# Seminario de Actualización

## Clase 02: Primera aplicación en Gradio

Interfaz web usando Gradio para crear interfaces gráficas para funciones de Python.

### app.py

- Posee una función saludar con los parámetros nombre e intensidad que devuelve un saludo con diferente cantidad de signos de exclamación según la intensidad elegida.

### Requisitos

- Python 3.13
- Dependencias listadas en requirements.txt

### Pasos

- Crear el entorno virtual:
  - python -m venv venv
  - Activarlo:
    - cmd: .\venv\Scripts\activate
    - Git Bash: source venv/Scripts/activate

  - Instalar las dependencias:
    - pip install -r requirements.txt

  - Ejecutar la app
    - Con el entorno virtual activado:
      - python app.py
      - Mostrará algo como:
        - Running on local URL: <http://127.0.0.1:7860>
      - Abrir esa URL en el navegador para probar la interfaz.
