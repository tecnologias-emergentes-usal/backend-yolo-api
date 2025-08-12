import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from ultralytics import YOLO
from confluent_kafka import Producer
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class YOLODetectionService:
    def __init__(self):
        self.kafka_config = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_PLAINTEXT'),
            'sasl.mechanisms': os.getenv('KAFKA_SASL_MECHANISMS', 'PLAIN'),
            'sasl.username': os.getenv('KAFKA_SASL_USERNAME', ''),
            'sasl.password': os.getenv('KAFKA_SASL_PASSWORD', '')
        }
        self.kafka_topic = os.getenv('KAFKA_TOPIC', 'predicciones')
        self.producer = Producer(self.kafka_config)
        
        # Configurar modelo
        self.model_path = self._get_model_path()
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {self.model_path}")
        
        self.model = YOLO(str(self.model_path))
        self.resultado_actual: List[Dict] = []
        
        logger.info(f"Servicio inicializado con modelo: {self.model_path}")
    
    def _get_model_path(self) -> Path:
        model_path = os.getenv('MODEL_PATH', 'modelos/best.pt')
        base_dir = Path(__file__).parent.parent
        return base_dir / model_path

    def procesar_imagen(self, ruta_imagen: str, cam_index: str) -> Dict:
        try:
            resultados = self.model(ruta_imagen)
            boxes = resultados[0].boxes
            
            predicciones = []
            if boxes is not None:
                for i in range(len(boxes)):
                    box = boxes[i]
                    predicciones.append({
                        "x1": float(box.xyxy[0][0]),
                        "y1": float(box.xyxy[0][1]),
                        "x2": float(box.xyxy[0][2]),
                        "y2": float(box.xyxy[0][3]),
                        "confidence": float(box.conf[0]),
                        "class_id": int(box.cls[0]),
                        "class_name": self.model.names[int(box.cls[0])]
                    })

            resultado_data = {
                "timestamp": datetime.now().isoformat(),
                "cam_index": cam_index,
                "predictions": predicciones
            }
            
            self.resultado_actual.append(resultado_data)
            self._enviar_kafka(resultado_data)
            self._limpiar_imagen(ruta_imagen)
            
            logger.info(f"Imagen procesada: {len(predicciones)} detecciones en cámara {cam_index}")
            return resultado_data
            
        except Exception as e:
            logger.error(f"Error procesando imagen {ruta_imagen}: {e}")
            raise
    
    def _enviar_kafka(self, resultado_data: Dict) -> None:
        try:
            self.producer.produce(self.kafka_topic, json.dumps(resultado_data).encode("utf-8"))
            self.producer.flush()
            logger.info(f"Predicción enviada a Kafka: {len(resultado_data['predictions'])} detecciones de cámara {resultado_data['cam_index']}")
        except Exception as e:
            logger.error(f"Error enviando a Kafka: {e}")
    
    def _limpiar_imagen(self, ruta_imagen: str) -> None:
        try:
            os.remove(ruta_imagen)
            logger.debug(f"Imagen eliminada: {ruta_imagen}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar {ruta_imagen}: {e}")

    def obtener_resultado(self) -> Optional[Dict]:
        if self.resultado_actual:
            return self.resultado_actual.pop(0)
        return None

# Instancia global del servicio
detection_service = YOLODetectionService()

# Funciones de compatibilidad
def procesar_imagen(ruta_imagen: str, cam_index: str) -> Dict:
    return detection_service.procesar_imagen(ruta_imagen, cam_index)

def obtener_resultado() -> Optional[Dict]:
    return detection_service.obtener_resultado()
