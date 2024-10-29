# Usa la imagen base de Ubuntu
FROM ubuntu:latest

# Actualiza el sistema e instala las dependencias
RUN apt-get update && apt install -y ffmpeg python3 python3-pip python3-flask

# Copia el archivo de la aplicación al contenedor
COPY app.py /app.py

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar el servidor
CMD ["python3", "/app.py"]
