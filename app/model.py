from ultralytics import YOLO

modelo = YOLO("modelos/best.pt")  # Cambiar por el modelo a evaluar

# Guarda el resultado más reciente
resultado_actual = [] #consumir de kafka

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

    # 👇 Guardar también el índice de cámara
    resultado_actual.append({
        "cam_index": cam_index,
        "predictions": predicciones
    })

    # ✅ Borrar imagen luego de procesarla
    import os
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

