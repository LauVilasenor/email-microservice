# 1. Imagen base de Python
FROM python:3.11-slim

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requerimientos
COPY requirements.txt .

# 4. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo tu código (incluyendo la carpeta app)
COPY . .

# 6. Puerto que usará el contenedor
EXPOSE 10000

# 7. Comando para encender tu FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]