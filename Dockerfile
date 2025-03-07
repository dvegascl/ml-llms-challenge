# Usar una imagen base de Python optimizada
FROM python:3.11

# Establecer el directorio de trabajo en la raíz del repo
WORKDIR /ml-llms-challenge

# Copiar todos los archivos al contenedor
COPY . /ml-llms-challenge/

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Asegurar que el modelo esté en el contenedor
COPY challenge/model.pkl /ml-llms-challenge/challenge/model.pkl

# Exponer el puerto en Render (IMPORTANTE: Render usa el puerto 10000 por defecto)
EXPOSE 10000

# Comando para iniciar la API
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "10000"]
