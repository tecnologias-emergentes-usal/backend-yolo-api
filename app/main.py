import logging
import os
import shutil
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.detection_service import procesar_imagen, obtener_resultado

load_dotenv()
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando servicio YOLO Detection API")
    upload_dir = Path(os.getenv('UPLOAD_DIR', 'static'))
    upload_dir.mkdir(exist_ok=True)
    yield
    logger.info("Cerrando servicio YOLO Detection API")

app = FastAPI(
    title="YOLO Detection API",
    description="API para detección de objetos usando YOLO con envío a Kafka",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', 'static'))

@app.post("/imagen")
async def recibir_imagen(
    file: UploadFile = File(...),
    cam_index: str = Form(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo requerido")
    
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Archivo debe ser una imagen")
    
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        resultado = procesar_imagen(str(file_path), cam_index)
        
        return JSONResponse({
            "status": "success",
            "message": "Imagen procesada correctamente",
            "cam_index": cam_index,
            "detections_count": len(resultado.get('predictions', []))
        })
        
    except Exception as e:
        logger.error(f"Error procesando imagen: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/resultado")
def resultado():
    try:
        result = obtener_resultado()
        if result is None:
            return JSONResponse(
                {"status": "no_data", "message": "No hay resultados disponibles"},
                status_code=204
            )
        return JSONResponse({
            "status": "success",
            "data": result
        })
    except Exception as e:
        logger.error(f"Error obteniendo resultado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "YOLO Detection API"}

@app.get("/")
def root():
    return {
        "service": "YOLO Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/imagen": "POST - Procesar imagen",
            "/resultado": "GET - Obtener último resultado",
            "/health": "GET - Estado del servicio"
        }
    }
