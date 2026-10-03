import gradio as gr


def saludar(nombre):
  if not nombre.strip():
    return "Por favor ingresá un nombre."
  return f"¡Hola, {nombre}! Bienvenido a la app con gr.Blocks."


def analizar_texto(texto):
    if not texto.strip():
        return "El texto está vacío.", 0, 0
    cant_caracteres = len(texto)
    cant_palabras = len(texto.split())
    resumen = f"El texto tiene {cant_palabras} palabras y {cant_caracteres} caracteres."
    return resumen, cant_palabras, cant_caracteres


with gr.Blocks(title="Demo Clase 4") as demo:
  gr.Markdown("#Mi primera App con Gradio Blocks")
  with gr.Tabs():
    with gr.Tab("Saludo"):
      with gr.Row():
        input_nombre = gr.Textbox(
            label="Tu nombre", placeholder="Escribí acá..."
        )
        output_saludo = gr.Textbox(label="Resultado", interactive=False)

      with gr.Row():
        btn_enviar = gr.Button("Saludar", variant="primary")
        btn_limpiar = gr.Button("Limpiar")

      btn_enviar.click(fn=saludar, inputs=input_nombre, outputs=output_saludo)
      btn_limpiar.click(
          fn=lambda: ("", ""), inputs=None, outputs=[input_nombre, output_saludo]
      )

    with gr.Tab("Analizador de texto"):
      with gr.Row():
        input_texto = gr.Textbox(
            label="Texto", placeholder="Escribí acá..."
        )
        output_resumen = gr.Textbox(label="Resultado", interactive=False)
        output_palabras = gr.Number(label="Cantidad de palabras", value=0, interactive=False)
        output_caracteres = gr.Number(label="Cantidad de caracteres", value=0, interactive=False)

      with gr.Row():
        btn_analizar = gr.Button("Analizar", variant="primary")
        btn_limpiar_texto = gr.Button("Limpiar")

      btn_analizar.click(
          fn=analizar_texto,
          inputs=input_texto,
          outputs=[output_resumen, output_palabras, output_caracteres],
      )
      btn_limpiar_texto.click(
          fn=lambda: ("", 0, 0),
          inputs=None,
          outputs=[output_resumen, output_palabras, output_caracteres],
      )

if __name__ == "__main__":
  demo.launch(share=True)