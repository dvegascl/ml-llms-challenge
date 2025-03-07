# Usar una imagen base de Python optimizada
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del repositorio al contenedor
COPY . /app/

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará la API
EXPOSE 10000

# Comando para iniciar la API en Render
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "10000"]
