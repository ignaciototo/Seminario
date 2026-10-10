from transformers import pipeline
import time
import pandas as pd

models = {
    "BERT-XNLI (110M)": "Recognai/bert-base-spanish-wwm-cased-xnli",
    "SELECTRA-Medium (38M)": "Recognai/zeroshot_selectra_medium"
}

labels = [
    "Recepción de Pallets",
    "Preparación de Pedidos",
    "Almacenamiento de pallets",
    "Expedición de Camiones",
    "Despacho de pedidos",
    "Planificación de viajes",
    "Control de Inventario",
    "Sistemas y Soporte WMS"
]

questions = [
    # Recepción de Pallets
    ("Estoy recepcionando un pale que tiene rotura. Como lo registro?", "Recepción de Pallets"),
    ("Los pallets que estamos descargando en la rece están fuera de estandar. Tengo que cobrar el retrabajo al proveedor. Que función de la PDA era?", "Recepción de Pallets"),
    
    # Planificación de viajes
    ("El plan quedó chico. Necesito que envien más volumen para replnificar. Sino van a quedar los camiones por la mitad.", "Planificación de viajes"),

    # Almacenamiento de pallets
    ("Terminé de descargar y la PDA me manda a guardar el pallet en el pasillo 14, pero la altura del hueco no da para este bulto. Como pido reubicarlo?", "Almacenamiento de pallets"),
    
    # Preparación de Pedidos
    ("En el Hueco no está el PLU que me dice la PDA que tengo que pickear. Como registro la incidencia?", "Preparación de Pedidos"),
    ("La repo de mercadería me envío a reponer a un hueco de picking que está lleno.", "Preparación de Pedidos"),
    
    # Expedición de Camiones
    ("Que función de la PDA es la que tengo que acceder para consolidar pallets pa subir al camión?", "Expedición de Camiones"),
    ("El camión está lleno pero la HDR tiene más pallets.", "Expedición de Camiones"),

    # Despacho de pedidos
    ("Estoy en el andén. Me falta cerrar el camión para que salga a la calle. Pero no se como se hace.", "Despacho de pedidos"),
    
    # Control de Inventario
    ("En el controlde rutina, detectamos diferencias entre el stock físico y lo que dice el wms. Me faltan 3 bultos del PLU 42222 en el rack", "Control de Inventario"),
    
    # Despacho de pedidos
    ("La PDA quiere consolidar pales de pollo con veneno para subirlos a un camión. Eso está mal.", "Despacho de pedidos"),
    
    # Sistemas y Soporte WMS
    ("La PDA está tirando error de conexión al WIFI.", "Sistemas y Soporte WMS")
]


results = []

for model_name, model_id in models.items():
    print(f"\n==============================================")
    print(f"Cargando {model_name}...")
    t0 = time.time()
    classifier = pipeline("zero-shot-classification", model=model_id, device=-1)
    load_time = time.time() - t0
    print(f"Modelo cargado en {load_time:.2f}s")

    for q, expected in questions:
        t_start = time.time()
        res = classifier(
            q,
            candidate_labels=labels,
            hypothesis_template="Esta consulta corresponde al área de {}."
        )
        infer_time = time.time() - t_start

        top_label = res["labels"][0]
        top_score = res["scores"][0]
        second_label = res["labels"][1]
        second_score = res["scores"][1]

        results.append({
            "Modelo": model_name,
            "Pregunta": q,
            "Esperada": expected,
            "Predicha": top_label,
            "Acierto": "SI" if top_label == expected else "NO",
            "Confianza": f"{top_score*100:.1f}%",
            "2da Opción": f"{second_label} ({second_score*100:.1f}%)",
            "Tiempo (s)": round(infer_time, 2)
        })

df = pd.DataFrame(results)
print("\n\n=== TABLA COMPARATIVA COMPLETA ===")
print(df.to_string(index=False))

try:
    df.to_csv("comparativa_modelos.csv", index=False)
    print("\nGuardado en comparativa_modelos.csv")
except PermissionError:
    df.to_csv("comparativa_modelos_nueva.csv", index=False)
    print("\ncomparativa_modelos.csv estaba en uso. Guardado en comparativa_modelos_nueva.csv")
