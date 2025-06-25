from ultralytics import YOLO
from kafka import KafkaProducer, KafkaConsumer
import json
import os
import time

# Configuración de Kafka
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'  # Para Docker
# KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Para desarrollo local
KAFKA_TOPIC = 'yolo-predictions'

# Variable para guardar el último resultado (como fallback si Kafka falla)
ultimo_resultado = None

# Inicializar productor Kafka
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Productor Kafka inicializado correctamente en {KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    print(f"Error al inicializar el productor Kafka: {e}")
    producer = None

modelo = YOLO("modelos/yolo11m-seg.pt")  # Cambiar por el modelo a evaluar

def procesar_imagen(ruta_imagen: str):
    """
    Procesa una imagen con el modelo YOLO y publica los resultados en Kafka
    """
    global ultimo_resultado
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

    # Guardar el resultado localmente como fallback
    resultado = {"predictions": predicciones}
    ultimo_resultado = resultado
    
    # Publicar en el tópico de Kafka si está disponible
    if producer:
        try:
            producer.send(KAFKA_TOPIC, resultado)
            producer.flush()  # Asegurarse de que el mensaje se envíe
            print(f"[Producer] Mensaje enviado al tópico {KAFKA_TOPIC}")
        except Exception as e:
            print(f"Error al enviar mensaje a Kafka: {e}")
    else:
        print("Productor Kafka no disponible, usando almacenamiento local")

    # ✅ Borrar imagen luego de procesarla
    try:
        os.remove(ruta_imagen)
        print(f"Imagen eliminada: {ruta_imagen}")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar la imagen: {ruta_imagen} ({e})")

def obtener_resultado():
    """
    Obtiene el último resultado de las predicciones desde Kafka o fallback local
    """
    global ultimo_resultado
    
    try:
        print(f"Intentando obtener resultado desde Kafka ({KAFKA_BOOTSTRAP_SERVERS})")
        
        # Crear un consumidor temporal para obtener el último mensaje
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',  # Obtener solo los mensajes más recientes
            group_id='yolo-predictions-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000  # Timeout después de 5 segundos si no hay mensajes
        )
        
        # Esperar a que Kafka esté disponible
        timeout = 5  # segundos
        start_time = time.time()
        while not consumer.bootstrap_connected() and time.time() - start_time < timeout:
            print("Esperando conexión con Kafka...")
            time.sleep(0.5)
            
        if not consumer.bootstrap_connected():
            print("No se pudo conectar con Kafka, usando resultado local")
            return ultimo_resultado
            
        print("[Consumer] Buscando mensajes en el tópico", KAFKA_TOPIC)
        
        # Intentar obtener el último mensaje
        mensaje = None
        for msg in consumer:
            mensaje = msg.value
            print(f"[Consumer] Mensaje recibido: {mensaje}")
            break  # Solo necesitamos el primer mensaje
            
        consumer.close()
        
        if mensaje:
            return mensaje
        else:
            print("No se encontraron mensajes en Kafka, usando resultado local")
            return ultimo_resultado
            
    except Exception as e:
        print(f"Error al consumir mensajes de Kafka: {e}")
        print("Usando resultado local como fallback")
        return ultimo_resultado
