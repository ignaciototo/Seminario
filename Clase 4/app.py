import gradio as gr


def saludar(nombre):
  if not nombre.strip():
    return "Por favor ingresá un nombre."
  return f"¡Hola, {nombre}! Bienvenido a la app con gr.Blocks."


with gr.Blocks(title="Demo Clase 4") as demo:
  gr.Markdown("# 🚀 Mi primera App con Gradio Blocks")
  gr.Markdown("Ejemplo interactivo para la Clase 4.")

  with gr.Row():
    input_nombre = gr.Textbox(
        label="Tu nombre", placeholder="Escribí acá..."
    )
    output_saludo = gr.Textbox(label="Resultado", interactive=False)

  btn_enviar = gr.Button("Saludar", variant="primary")
  btn_limpiar = gr.Button("Limpiar")

  btn_enviar.click(fn=saludar, inputs=input_nombre, outputs=output_saludo)
  btn_limpiar.click(
      fn=lambda: ("", ""), inputs=None, outputs=[input_nombre, output_saludo]
  )

if __name__ == "__main__":
  demo.launch()