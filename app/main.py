from fastapi import FastAPI, UploadFile, File
from app.model import procesar_imagen, obtener_resultado
import os, shutil

app = FastAPI()
UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/imagen")
async def recibir_imagen(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    procesar_imagen(file_path)
    return {"status": "ok", "mensaje": "Imagen procesada"}

@app.get("/resultado")
def resultado():
    return obtener_resultado()
