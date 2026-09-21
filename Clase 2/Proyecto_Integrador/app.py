import gradio as gr


def saludar(nombre, intensidad):
  return "¡Hola " + nombre + "!" * int(intensidad)


demo = gr.Interface(
    fn=saludar,
    inputs=["text", gr.Slider(1, 5, value=1, step=1, label="Intensidad")],
    outputs="text",
    title="Ejemplo Básico de Gradio",
    description="Escribí tu nombre y elegí cuántas veces querés que te salude.",
)

if __name__ == "__main__":
  demo.launch()