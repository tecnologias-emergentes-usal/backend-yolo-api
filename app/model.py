import os
from ultralytics import YOLO
from confluent_kafka import Producer
import json

# Configuración Kafka
KAFKA_CONF = {
    'bootstrap.servers': '138.197.10.213:30083',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'user1',
    'sasl.password': 'ACW7Ut9Xv6'
}
KAFKA_TOPIC = 'predicciones'
producer = Producer(KAFKA_CONF)

# Ruta del modelo
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ruta_modelo = os.path.join(BASE_DIR, "modelos", "best.pt")

if not os.path.exists(ruta_modelo):
    raise FileNotFoundError(f"No se encontró el modelo en: {ruta_modelo}")

modelo = YOLO(ruta_modelo)
resultado_actual = []

def procesar_imagen(ruta_imagen: str, cam_index: str):
    global resultado_actual
    resultados = modelo(ruta_imagen)
    boxes = resultados[0].boxes

    predicciones = []
    for i in range(len(boxes)):
        box = boxes[i]
        predicciones.append({
            "x1": float(box.xyxy[0][0]),
            "y1": float(box.xyxy[0][1]),
            "x2": float(box.xyxy[0][2]),
            "y2": float(box.xyxy[0][3]),
            "confidence": float(box.conf[0]),
            "class_id": int(box.cls[0]),
            "class_name": modelo.names[int(box.cls[0])]
        })

    # Guardar localmente
    resultado_actual.append({
        "cam_index": cam_index,
        "predictions": predicciones
    })

    # Enviar a Kafka
    try:
        mensaje = {
            "cam_index": cam_index,
            "predictions": predicciones
        }
        producer.produce(KAFKA_TOPIC, json.dumps(mensaje).encode("utf-8"))
        producer.flush()
        print(f"[Kafka] Mensaje enviado al tópico '{KAFKA_TOPIC}'")
    except Exception as e:
        print(f"⚠️ Error al enviar a Kafka: {e}")

    # Borrar imagen
    try:
        os.remove(ruta_imagen)
        print(f"Imagen eliminada: {ruta_imagen}")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar la imagen: {ruta_imagen} ({e})")

def obtener_resultado():
    if resultado_actual:
        return resultado_actual.pop(0)
    else:
        return None
