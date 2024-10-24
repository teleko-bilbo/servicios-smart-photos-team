# Usa la última versión de Ubuntu como imagen base
FROM ubuntu:latest

# Instala FFmpeg y las dependencias de Python, incluyendo Flask
RUN apt update && apt install -y ffmpeg python3 python3-flask

# Crea el directorio de trabajo
WORKDIR /app

# Copia tu script Flask dentro del contenedor
COPY app.py /app

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Define el comando de inicio del contenedor
CMD ["python3", "app.py"]

