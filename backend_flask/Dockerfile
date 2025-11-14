# Imagen base con Python
FROM python:3.13-slim

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY app /app/app

# Exponer puerto
EXPOSE 5000

# Comando de ejecución
CMD ["python", "-m", "app"]
