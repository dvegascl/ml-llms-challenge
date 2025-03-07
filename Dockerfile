# Usar una imagen base de Python optimizada
FROM python:3.11

# Establecer el directorio de trabajo en la raíz del contenedor
WORKDIR /app

# Copiar todos los archivos del repositorio al contenedor
COPY . /app/

# Cambiar al directorio donde está la API
WORKDIR /app/challenge

# Instalar las dependencias desde requirements.txt (ubicado en /app/)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponer el puerto que usará la API
EXPOSE 10000

# Comando para iniciar la API en Render
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
