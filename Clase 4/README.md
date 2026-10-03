# Seminario de Actualización

## Clase 04: Modificar la interfaz con Blocks

Modificar la interfaz usando Blocks e incorporar nuevos componenetes y funciones:

### app.py

- Posee una función saludar que recibe un nombre por parámetro y devuelve un saludo.
- Posee una función analizar_texto que recibe un texto por parámetro y devuelve un resumen del texto, la cantidad de palabras y la cantidad de caracteres.

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
