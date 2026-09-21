# Clase 05: Publicación y Comparativa de Deploys

### Links de las aplicaciones
- **Gradio en Render:** [TU_LINK_DE_RENDER](https://tu-app.onrender.com)
- **Streamlit Community Cloud:** [TU_LINK_DE_STREAMLIT](https://tu-app.streamlit.app)

### Diferencias encontradas en el despliegue
- **Flujo de ejecución:** Gradio maneja el ciclo de vida mediante funciones y eventos explícitos (`btn.click`), mientras que Streamlit reejecuta el script completo de arriba a abajo ante cada interacción.
- **Configuración del servidor:** En Render hubo que configurar el puerto dinámico de red (`0.0.0.0` y variable `PORT`) y especificar el *Root Directory* del monorepo. En cambio, Streamlit Cloud se integra de forma nativa con GitHub permitiendo apuntar directamente a la ruta del archivo `Clase_05/app_streamlit.py` sin configuración adicional de servidores ni puertos.