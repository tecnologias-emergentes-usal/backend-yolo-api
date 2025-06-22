# 📝 Backlog Proyecto YOLOv8 - Toy Cars Detection
**Equipo:** Tomas Vicente & Fausto Buzzeti

---

## 1. Armado y limpieza de datasets

- **Descarga y análisis de tres datasets:**
    - Uno multiclase (Ambulance, Bike, Bus, Car, Truck).
    - Uno single-class ("car") sin splits.
    - **Uno hecho manualmente por compañeros y etiquetado manualmente.**
- **Estandarización de estructura:**  
    - Todos los datasets convertidos a formato YOLO: imágenes `.jpg/.png` + labels `.txt` con bounding boxes.
    - Se verificó el dataset manual y se corrigieron formatos si fue necesario para que coincidieran con el estándar.

---

## 2. Procesamiento de datasets

- **Script para dividir los datasets single-class y manual** en splits `train`, `valid` y `test` de manera aleatoria y proporcional (70%-20%-10%), generando la estructura `/train/images`, `/train/labels`, etc.
- **Chequeo de integridad:**  
    - Se revisó que el dataset manual estuviera correctamente anotado y no tuviera archivos huérfanos.
    - Se consolidó el naming y formato de todas las etiquetas.

---

## 3. Limpieza del dataset multiclase

- **Conversión a single-class:**  
    - Se filtraron las etiquetas para dejar solo la clase "car" (ID=3), convirtiendo todas las anotaciones a clase "0" y eliminando los demás objetos de cada label.
- **Revisión de labels:**  
    - Se aplicó una función de limpieza para asegurar la unicidad de la clase.

---

## 4. Fusión de datasets

- **Merge script:**  
    - Se fusionaron los tres datasets (multiclase convertido, single-class, manual) en una carpeta combinada, evitando duplicados de nombre (con prefijos si era necesario).
- **Chequeo de integridad:**  
    - Verificación de la cantidad de imágenes y labels en cada split después de sumar el dataset manual.

---

## 5. Generación de archivo de configuración

- **Creación del `data.yaml`** para YOLOv8, apuntando a las rutas correctas de train/valid/test e indicando la clase `car` y cantidad de clases `nc: 1`.

---

## 6. Entrenamiento inicial de YOLOv8

- **Primer entrenamiento:**  
    - Modelo base: `yolov8n.pt`
    - Dataset combinado (los tres datasets), 30 epochs.
    - Chequeo de métricas y matriz de confusión.

---

## 7. Análisis de resultados y backlog de mejoras

- **Interpretación de matriz de confusión:**  
    - Se identificó errores de falsos positivos/negativos.
- **Recomendaciones:**  
    - Mejorar calidad de datos, usar más augmentations, limpiar anotaciones, ajustar hiperparámetros.

---

## 8. Fine-tuning y mejoras

- **Reentrenamiento incremental:**  
    - A partir de `best.pt` anterior, con las imágenes mejoradas y más augmentations.
    - Se aumentó a 50 epochs.
    - Se configuró `save_period=5` para checkpoints frecuentes.

---

## 9. Validación y evaluación final

- **Evaluación con `yolo val`:**  
    - Se obtuvieron matriz de confusión y métricas.
- **Confirmación:**  
    - El archivo `best.pt` se identificó como el modelo óptimo.

---

## 10. Exportación y despliegue

- **Guía de uso del modelo fuera de Colab:**  
    - Uso en tiempo real con cámara, exportación a ONNX/TensorRT.
- **Instrucciones de inferencia en cualquier entorno con Ultralytics y Python.**

---

## 11. Lecciones aprendidas y recomendaciones

- **El valor de sumar datos manualmente etiquetados:** mejoró mucho la robustez y generalización del modelo.
- **Automatización de splits y limpieza para futuros proyectos.**
- **Reanudar entrenamientos y prevenir pérdidas en plataformas cloud.**

---

### Estado actual:

- Modelo `best.pt` entrenado, validado y listo para uso en tiempo real.
- Dataset combinado y curado (incluyendo datos manuales).
- Flujo portable para futuros proyectos YOLO.

