# Se utiliza una imagen oficial de Python 'slim'.
FROM python:3.9-slim

# Se instalan las dependencias de sistema requeridas por OpenCV.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --- CAMBIO ESTRUCTURAL CLAVE ---
# Se establece el WORKDIR en la raíz del proyecto, NO en la carpeta de la app.
WORKDIR /project

# Se copian e instalan los requerimientos de Python.
# Esto se hace en la raíz del proyecto.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Se copia TODO el contenido del proyecto (la carpeta 'app', 'modelos', etc.)
# al WORKDIR (/project).
COPY . .

# Se expone el puerto que usará uvicorn.
EXPOSE 8000

# --- CMD CORREGIDO Y FINAL ---
# Se ejecuta uvicorn desde el WORKDIR (/project).
# Ahora Python PUEDE encontrar el paquete 'app' porque existe la ruta /project/app/
# El comando 'app.main:app' es ahora correcto.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
