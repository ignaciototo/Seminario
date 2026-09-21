import os
import gradio as gr

def generar_saludo_personalizado(nombre, intensidad):
    if not nombre.strip():
        nombre = "amigo"

    signos = "!" * int(intensidad)
    return f"¡Hola {nombre}{signos}"


with gr.Blocks(title="Generador de Saludos con Blocks") as demo:
    gr.Markdown("# 👋 Generador de Saludos Personalizado")
    gr.Markdown("Ingresá tu nombre y seleccioná el nivel de entusiasmo.")

    with gr.Row():
        with gr.Column():
            input_nombre = gr.Textbox(
                label="Tu nombre",
                placeholder="Ingresar nombre"
            )

            input_intensidad = gr.Slider(
                minimum=1,
                maximum=5,
                value=1,
                step=1,
                label="Nivel de entusiasmo"
            )

            btn_saludar = gr.Button(
                "Generar Saludo",
                variant="primary"
            )

        with gr.Column():
            output_saludo = gr.Textbox(label="Resultado")

    btn_saludar.click(
        fn=generar_saludo_personalizado,
        inputs=[input_nombre, input_intensidad],
        outputs=output_saludo
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )