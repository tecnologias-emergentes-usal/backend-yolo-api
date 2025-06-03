from ultralytics import YOLO

modelo = YOLO("modelos/yolov8n.pt")  # Cambiar por el modelo a evaluar

# Guarda el resultado más reciente
resultado_actual = []

def procesar_imagen(ruta_imagen: str):
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

    resultado_actual.append({"predictions": predicciones})

def obtener_resultado():
    if resultado_actual:
    	return resultado_actual.pop(0)
    else:
    	return None
