import os
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError

# Leemos el token del archivo .env
token = None
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.startswith("HF_TOKEN="):
                token = line.strip().split("=", 1)[1]

if not token or token == "hf_tu_token_aqui":
    print("=" * 60)
    print("⚠️  AVISO: No se encontró un token válido de Hugging Face.")
    print("Para probar la API de inferencia externa:")
    print("1. Renombra .env.example a .env")
    print("2. En .env, ingresa tu token personal (https://huggingface.co/settings/tokens)")
    print("=" * 60)
    exit(0)

print(f"Usando token: {token[:6]}...{token[-4:]}\n")

client = InferenceClient(token=token)

models = [
    ("Recognai/bert-base-spanish-wwm-cased-xnli", "Error 402: Payment Required"),
    ("Recognai/zeroshot_selectra_medium", "Error: StopIteration (Sin provider en HF Router)")
]

for model_id, expected_behavior in models:
    print("=" * 60)
    print(f"Probando: {model_id}")
    print(f"Comportamiento esperado: {expected_behavior}")
    print("=" * 60)
    try:
        res = client.zero_shot_classification(
            text="Llegó un pale con rotura. Como lo registro?",
            candidate_labels=["Recepción", "Expedición", "Inventario"],
            hypothesis_template="Esta consulta corresponde al área de {}.",
            model=model_id
        )
        print("Resultado exitoso:", res)
    except HfHubHTTPError as e:
        print("\n--> [ERROR CAPTURADO DE HUGGING FACE]:")
        print(f"Status Code: {e.response.status_code}")
        print(f"Mensaje del servidor: {e}")
    except Exception as e:
        print(f"\n--> [EXCEPCIÓN CAPTURADA]: {type(e).__name__}: {e}")
    print("\n")
