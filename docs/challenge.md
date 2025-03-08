# Desafío de Software Engineer (ML & LLMs) ESPAÑOL. Mas abajo estara la version en ingles

Este documento detalla la implementación del desafío, describiendo el proceso de desarrollo, las decisiones de diseño y las soluciones implementadas para cada parte del proyecto.

## Parte 1: Implementación del Modelo de Predicción de Retrasos

### Enfoque y Decisiones de Diseño

Para esta parte del desafío, he implementado un modelo de machine learning capaz de predecir si un vuelo tendrá retraso basándose en características como la aerolínea, el tipo de vuelo y el mes de operación. Las principales decisiones de diseño fueron:

1. **Selección del Modelo**: Elegí XGBoost como algoritmo principal debido a su buen rendimiento en el notebook de exploración. El modelo mostró un equilibrio adecuado entre precisión y recall para la detección de retrasos.

2. **Características Importantes**: Después de analizar el notebook de exploración, identifiqué las 10 características más importantes para la predicción, incluyendo aerolíneas específicas (como Latin American Wings y Grupo LATAM) y meses de alta demanda.

3. **Balanceo de Clases**: Implementé balanceo de clases mediante el parámetro `scale_pos_weight` para manejar la distribución desigual entre vuelos con y sin retraso.

4. **Preprocesamiento de Datos**: Desarrollé funciones robustas para calcular variables derivadas como `min_diff`, `high_season` y `period_day`, siguiendo los criterios establecidos en el notebook original.

### Mejoras sobre el Notebook Original

1. **Código Modularizado**: Convertí el código del notebook en una clase bien estructurada (`DelayModel`) con métodos claros para preprocesamiento, entrenamiento y predicción.

2. **Manejo de Errores**: Incorporé manejo de excepciones robusto para evitar fallos en casos límite y datos inconsistentes.

3. **Optimización de Rendimiento**: Refiné el proceso de selección de características para reducir la dimensionalidad y mejorar el tiempo de entrenamiento y predicción.

4. **Documentación**: Agregué docstrings detallados y comentarios explicativos para facilitar el mantenimiento y comprensión del código.

## Parte 2: Implementación de la API con FastAPI

### Estructura de la API

Implementé una API RESTful utilizando FastAPI que expone dos endpoints principales:

1. **GET /health**: Endpoint para verificar el estado operativo de la API.
   - Responde con `{"status": "OK"}` cuando la API está funcionando correctamente.

2. **POST /predict**: Endpoint para realizar predicciones de retrasos en vuelos.
   - Recibe un JSON con una lista de vuelos, cada uno con los campos OPERA, TIPOVUELO y MES.
   - Retorna una lista de predicciones (1 para retraso, 0 para vuelo a tiempo).

### Validación de Datos

Para asegurar la integridad de los datos y facilitar el uso de la API:

1. Implementé validadores para cada campo de entrada:
   - MES: Debe ser un entero entre 1 y 12
   - TIPOVUELO: Debe ser "I" (Internacional) o "N" (Nacional)
   - OPERA: Debe ser una aerolínea válida de la lista predefinida

2. Diseñé esquemas Pydantic para la validación automática de la estructura de las solicitudes y respuestas.

3. Configuré manejo de errores para proporcionar mensajes claros cuando los datos de entrada no cumplen los requisitos.

### Integración con el Modelo

La API carga el modelo preentrenado al inicio y lo utiliza para realizar predicciones en tiempo real:

1. Cada solicitud a `/predict` convierte los datos recibidos a un DataFrame de pandas.
2. Los datos son preprocesados utilizando el mismo pipeline implementado en `model.py`.
3. El modelo realiza la predicción y devuelve los resultados.

## Parte 3: Despliegue en Google Cloud Platform

### Arquitectura de la Solución

La solución se desplegó en Google Cloud Platform utilizando los siguientes servicios:

1. **Cloud Run**: Para alojar la API como un servicio serverless, aprovechando su escalabilidad automática y modelo de pago por uso.

2. **Container Registry**: Para almacenar la imagen Docker de la aplicación.

3. **Cloud Build**: Para automatizar el proceso de construcción de la imagen Docker.

### Proceso de Despliegue

El proceso de despliegue se realizó siguiendo estos pasos:

1. **Containerización**: Creé un Dockerfile para empaquetar la aplicación y sus dependencias.

2. **Construcción de la Imagen**: Utilicé Google Cloud Build para construir la imagen Docker a partir del Dockerfile.

3. **Despliegue en Cloud Run**: Desplegué la imagen en Cloud Run, configurando el servicio para que sea accesible públicamente sin autenticación.

4. **Configuración de Recursos**: Asigné recursos adecuados (memoria, CPU) para garantizar un rendimiento óptimo de la API.

### URL de la API Desplegada

La API está desplegada y accesible en la siguiente URL:
https://delay-prediction-api-461426734233.us-central1.run.app

Ejemplos de uso:

1. Verificación de estado:
```bash
curl https://delay-prediction-api-461426734233.us-central1.run.app/health
```


2. Predicción de retraso:
```bash
curl -X POST \
  https://delay-prediction-api-461426734233.us-central1.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "OPERA": "Grupo LATAM",
        "TIPOVUELO": "I",
        "MES": 7
      }
    ]
  }'
  ```
# Parte 4: Configuración de CI/CD

## Pipeline de Integración Continua
Configuré un pipeline de integración continua en GitHub Actions que se ejecuta en cada push a las ramas `develop` y `feature/*`, y en cada pull request a `main`. El workflow realiza las siguientes tareas:

1. **Configuración del Entorno**: Configura un entorno Python 3.9 y instala todas las dependencias necesarias.
2. **Pruebas del Modelo**: Ejecuta las pruebas del modelo para verificar su correcta implementación.
3. **Pruebas de la API**: Ejecuta las pruebas de la API para garantizar que los endpoints funcionan según lo esperado.
4. **Generación de Informes**: Genera y sube informes de pruebas como artefactos para su posterior análisis.

## Pipeline de Entrega Continua
Implementé un pipeline de entrega continua que se activa en cada push a la rama `main`. El workflow realiza las siguientes tareas:

1. **Autenticación en GCP**: Utiliza credenciales seguras almacenadas como secretos de GitHub para autenticarse en Google Cloud Platform.
2. **Construcción y Despliegue**: Construye una nueva imagen Docker y la despliega automáticamente en Cloud Run.
3. **Actualización de URL**: Actualiza la URL de la API en el Makefile para las pruebas de estrés.
4. **Pruebas de Estrés**: Ejecuta pruebas de estrés contra la API recién desplegada para verificar su rendimiento bajo carga.

## Seguridad
Para garantizar la seguridad de las credenciales y otros datos sensibles:

- Almacené las credenciales de GCP como secretos en GitHub (`GCP_PROJECT_ID` y `GCP_SA_KEY`).
- Configuré los permisos adecuados para la cuenta de servicio en GCP, siguiendo el principio de mínimo privilegio.
- Implementé validación y sanitización de datos en la API para prevenir ataques.

## Conclusiones y Posibles Mejoras
La implementación actual cumple con todos los requisitos del desafío, proporcionando una solución completa para la predicción de retrasos en vuelos. Algunas posibles mejoras para el futuro incluyen:

- **Mejoras en el Modelo**: Experimentar con técnicas más avanzadas de feature engineering y diferentes algoritmos de machine learning.
- **Optimización de Rendimiento**: Implementar caché para mejorar el tiempo de respuesta de la API en consultas frecuentes.
- **Monitoreo y Logging**: Integrar soluciones de monitoreo y logging más completas para facilitar la detección y resolución de problemas.
- **Entrenamiento Automático**: Implementar un pipeline de entrenamiento automático que actualice periódicamente el modelo con nuevos datos.
- **Documentación Interactiva**: Mejorar la documentación de la API con ejemplos interactivos y una interfaz de usuario para facilitar pruebas.

Este proyecto demuestra la capacidad de implementar soluciones end-to-end para problemas de machine learning, desde el desarrollo del modelo hasta su despliegue en producción, siguiendo buenas prácticas de ingeniería de software y DevOps.

# Software Engineer Challenge (ML & LLMs) ENGLISH

This document details the implementation of the challenge, describing the development process, design decisions, and solutions implemented for each part of the project.

## Part 1: Implementation of the Delay Prediction Model

### Approach and Design Decisions

For this part of the challenge, I implemented a machine learning model capable of predicting if a flight will be delayed based on features such as the airline, flight type, and operating month. The main design decisions were:

1. **Model Selection**: I chose XGBoost as the main algorithm due to its good performance in the exploration notebook. The model showed a suitable balance between precision and recall for delay detection.

2. **Important Features**: After analyzing the exploration notebook, I identified the 10 most important features for prediction, including specific airlines (such as Latin American Wings and Grupo LATAM) and high-demand months.

3. **Class Balancing**: I implemented class balancing using the `scale_pos_weight` parameter to handle the unequal distribution between flights with and without delays.

4. **Data Preprocessing**: I developed robust functions to calculate derived variables such as `min_diff`, `high_season`, and `period_day`, following the criteria established in the original notebook.

### Improvements Over the Original Notebook

1. **Modularized Code**: I converted the notebook code into a well-structured class (`DelayModel`) with clear methods for preprocessing, training, and prediction.

2. **Error Handling**: I incorporated robust exception handling to prevent failures in edge cases and inconsistent data.

3. **Performance Optimization**: I refined the feature selection process to reduce dimensionality and improve training and prediction time.

4. **Documentation**: I added detailed docstrings and explanatory comments to facilitate code maintenance and understanding.

## Part 2: Implementation of the API with FastAPI

### API Structure

I implemented a RESTful API using FastAPI that exposes two main endpoints:

1. **GET /health**: Endpoint to check the operational status of the API.
   - Responds with `{"status": "OK"}` when the API is functioning correctly.

2. **POST /predict**: Endpoint to make flight delay predictions.
   - Receives a JSON with a list of flights, each with the fields OPERA, TIPOVUELO, and MES.
   - Returns a list of predictions (1 for delay, 0 for on-time flight).

### Data Validation

To ensure data integrity and facilitate API usage:

1. I implemented validators for each input field:
   - MES: Must be an integer between 1 and 12
   - TIPOVUELO: Must be "I" (International) or "N" (National)
   - OPERA: Must be a valid airline from the predefined list

2. I designed Pydantic schemas for automatic validation of request and response structures.

3. I configured error handling to provide clear messages when input data does not meet requirements.

### Integration with the Model

The API loads the pretrained model at startup and uses it for real-time predictions:

1. Each request to `/predict` converts the received data to a pandas DataFrame.
2. The data is preprocessed using the same pipeline implemented in `model.py`.
3. The model makes the prediction and returns the results.

## Part 3: Deployment on Google Cloud Platform

### Solution Architecture

The solution was deployed on Google Cloud Platform using the following services:

1. **Cloud Run**: To host the API as a serverless service, taking advantage of its automatic scaling and pay-per-use model.

2. **Container Registry**: To store the Docker image of the application.

3. **Cloud Build**: To automate the process of building the Docker image.

### Deployment Process

The deployment process was carried out following these steps:

1. **Containerization**: I created a Dockerfile to package the application and its dependencies.

2. **Image Building**: I used Google Cloud Build to build the Docker image from the Dockerfile.

3. **Deployment on Cloud Run**: I deployed the image on Cloud Run, configuring the service to be publicly accessible without authentication.

4. **Resource Configuration**: I allocated adequate resources (memory, CPU) to ensure optimal API performance.

### Deployed API URL

The API is deployed and accessible at the following URL:
https://delay-prediction-api-461426734233.us-central1.run.app

Usage examples:

1. Health check:
```bash
curl https://delay-prediction-api-461426734233.us-central1.run.app/health
```

2. Delay prediction:
```bash
curl -X POST \
  https://delay-prediction-api-461426734233.us-central1.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "OPERA": "Grupo LATAM",
        "TIPOVUELO": "I",
        "MES": 7
      }
    ]
  }'
```

## Part 4: CI/CD Configuration

### Continuous Integration Pipeline
I configured a continuous integration pipeline in GitHub Actions that runs on each push to the `develop` and `feature/*` branches, and on each pull request to `main`. The workflow performs the following tasks:

1. **Environment Setup**: Sets up a Python 3.9 environment and installs all necessary dependencies.
2. **Model Testing**: Runs model tests to verify its correct implementation.
3. **API Testing**: Runs API tests to ensure that the endpoints work as expected.
4. **Report Generation**: Generates and uploads test reports as artifacts for later analysis.

### Continuous Delivery Pipeline
I implemented a continuous delivery pipeline that is triggered on each push to the `main` branch. The workflow performs the following tasks:

1. **GCP Authentication**: Uses secure credentials stored as GitHub secrets to authenticate in Google Cloud Platform.
2. **Build and Deployment**: Builds a new Docker image and automatically deploys it to Cloud Run.
3. **URL Update**: Updates the API URL in the Makefile for stress tests.
4. **Stress Testing**: Runs stress tests against the newly deployed API to verify its performance under load.

### Security
To ensure the security of credentials and other sensitive data:

- I stored GCP credentials as secrets in GitHub (`GCP_PROJECT_ID` and `GCP_SA_KEY`).
- I configured appropriate permissions for the service account in GCP, following the principle of least privilege.
- I implemented data validation and sanitization in the API to prevent attacks.

### Conclusions and Possible Improvements
The current implementation meets all the challenge requirements, providing a complete solution for flight delay prediction. Some possible improvements for the future include:

- **Model Improvements**: Experiment with more advanced feature engineering techniques and different machine learning algorithms.
- **Performance Optimization**: Implement caching to improve API response time for frequent queries.
- **Monitoring and Logging**: Integrate more comprehensive monitoring and logging solutions to facilitate problem detection and resolution.
- **Automatic Training**: Implement an automatic training pipeline that periodically updates the model with new data.
- **Interactive Documentation**: Enhance API documentation with interactive examples and a user interface to facilitate testing.

This project demonstrates the ability to implement end-to-end solutions for machine learning problems, from model development to production deployment, following good software engineering and DevOps practices.

