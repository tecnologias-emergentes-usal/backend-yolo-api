# YoloAPIProject

API REST desarrollada con **FastAPI** que permite enviar una imagen a un modelo **YOLOv8 preentrenado** y obtener las predicciones en formato JSON. El modelo se ejecuta en backend y el resultado puede ser consultado por cualquier frontend o sistema externo.

---

## 📦 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- Entorno virtual recomendado (venv)
- Conexión a internet (para descargar el modelo YOLO si no está en local)
- Docker y Docker Compose (para ejecutar Kafka)

---

## ⚙️ Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/tecnologias-emergentes-usal/backend-yolo-api.git
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

> Esto incluye: `fastapi`, `uvicorn`, `ultralytics`, `kafka-python`

4. **(Opcional) Descargar manualmente el modelo:**

Si querés tener el archivo `.pt` en el proyecto:

- Descargar desde: [YOLOv8n.pt](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt)
- Guardarlo en la carpeta: `modelos/yolov8n.pt`

---

## 🚀 Cómo correr la API

### 1. Iniciar Kafka y Zookeeper

Desde la raíz del proyecto:

```bash
docker-compose up -d
```

Esto iniciará:
- Zookeeper en el puerto 2181
- Kafka en el puerto 9092
- Kafdrop (interfaz web para Kafka) en el puerto 9000
- API YOLO en el puerto 8000

Puedes acceder a la interfaz de Kafdrop en `http://localhost:9000` para monitorear los tópicos y mensajes de Kafka.

### 2. Iniciar la API (si no usas Docker)

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

Esto procesa la imagen con el modelo YOLO y publica las predicciones en el tópico de Kafka.

### 2. Consultar el resultado (GET)

Ir a `/resultado` y hacer clic en "Execute"  
Se devuelve un JSON con todas las detecciones desde Kafka:

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
│   ├── model.py         # Procesamiento YOLO y Kafka
│   └── __init__.py
├── modelos/             # Modelo YOLO (.pt)
├── static/              # Imágenes temporales
├── requirements.txt     # Dependencias
├── docker-compose.yml   # Configuración de Kafka y Zookeeper
├── wait-for-kafka.sh    # Script para esperar a Kafka
├── Dockerfile           # Configuración para Docker
```

---

## 📌 Notas

- Se actualizo al modelo "yolo11m-seg.pt" con el cual el equipo de IA realizo las pruebas.
- Las predicciones ahora se publican en un tópico de Kafka llamado 'yolo-predictions'.
- Cada usuario puede suscribirse al tópico de Kafka para recibir las predicciones.
- Se incluye Kafdrop como interfaz web para monitorear los tópicos y mensajes de Kafka.
- Si Kafka no está disponible, se utiliza un almacenamiento local como fallback.

---

## 🧠 Autores

Desarrollado por Federico Stragliati y equipo Infraestructura.  
[GitHub](https://github.com/federicostragliati)
[GitHub](https://github.com/GermanUSAL)
[GitHub](https://github.com/ramoswilly)

Integración con Kafka por el equipo de Mensajería de Colas.

