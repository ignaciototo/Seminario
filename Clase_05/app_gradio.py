import os
import gradio as gr


def saludar(nombre):
  return f"¡Hola {nombre}! App corriendo en Render."


with gr.Blocks(title="Clase 05 - Gradio") as demo:
  gr.Markdown("# Gradio Blocks en Render")
  nombre = gr.Textbox(label="Nombre")
  salida = gr.Textbox(label="Resultado")
  btn = gr.Button("Enviar")
  btn.click(fn=saludar, inputs=nombre, outputs=salida)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 7860))
  demo.queue().launch(
      server_name="0.0.0.0",
      server_port=port,
      prevent_thread_lock=False,
  )