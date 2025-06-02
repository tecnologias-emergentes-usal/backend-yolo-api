# YoloAPIProject

API REST desarrollada con **FastAPI** que permite enviar una imagen a un modelo **YOLOv8 preentrenado** y obtener las predicciones en formato JSON. El modelo se ejecuta en backend y el resultado puede ser consultado por cualquier frontend o sistema externo.

---

## 📦 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- Entorno virtual recomendado (venv)
- Conexión a internet (para descargar el modelo YOLO si no está en local)

---

## ⚙️ Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/federicostragliati/YoloAPIProject.git
cd YoloAPIProject
```

2. **Crear entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate        # Windows
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
sudo apt install -y libgl1 # En Linux
```

> Esto incluye: `fastapi`, `uvicorn`, `ultralytics`

4. **(Opcional) Descargar manualmente el modelo:**

Si querés tener el archivo `.pt` en el proyecto:

- Descargar desde: [YOLOv8n.pt](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt)
- Guardarlo en la carpeta: `modelos/yolov8n.pt`

---

## 🚀 Cómo correr la API

Desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

- Acceder a la documentación automática de Swagger:
  ```
  http://localhost:8000/docs
  ```

---

## 🔁 Cómo probar

### 1. Subir una imagen (POST)

Usar Swagger UI:

- Ir a `/imagen`
- Cargar un archivo (campo `file`)
- Hacer clic en "Execute"

Esto procesa la imagen con el modelo YOLO.

### 2. Consultar el resultado (GET)

Ir a `/resultado` y hacer clic en "Execute"  
Se devuelve un JSON con todas las detecciones:

```json
{
  "predictions": [
    {
      "x1": 123.4,
      "y1": 45.6,
      "x2": 200.8,
      "y2": 300.9,
      "confidence": 0.87,
      "class_id": 16,
      "class_name": "dog"
    }
  ]
}
```

---

## 📁 Estructura del proyecto

```
YoloAPIProject/
├── app/
│   ├── main.py          # API FastAPI
│   ├── model.py         # Procesamiento YOLO
│   └── __init__.py
├── modelos/             # Modelo YOLO (.pt)
├── static/              # Imágenes temporales
├── requirements.txt     # Dependencias
```

---

## 📌 Notas

- Se actualizo al modelo "yolo11m-seg.pt" con el cual el equipo de IA realizo las pruebas.
- No se guarda el historial. Cada nueva imagen sobreescribe el resultado anterior.
- No se realiza validación de tipo de archivo aún.

---

## 🧠 Autor

Desarrollado por Federico Stragliati y equipo Infraestructura.  
[GitHub](https://github.com/federicostragliati)
