# Imagen base con Python
FROM python:3.13-slim

# Crear y usar el directorio de la app
WORKDIR /app

# Copiar dependencias
COPY src/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY src /app


# Exponer el puerto del backend
EXPOSE 5000

# Comando para ejecutar Flask
CMD ["python", "app.py"]

