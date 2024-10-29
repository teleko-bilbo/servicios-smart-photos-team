# V1:
# Sfrom flask import Flask
# import subprocess
# import os

# app = Flask(__name__)

# @app.route('/convert', methods=['GET'])
# def convert_video():
#     input_video = '/data/input_video.mp4'  # Cambia por tu nombre de video
#     output_video = '/data/output_video.avi'
#     command = ['ffmpeg', '-i', input_video, '-vf', 'scale=1920:1080', '-c:v', 'libx264', '-c:a', 'copy', output_video]

#     # Ejecuta el comando ffmpeg
#     subprocess.run(command, check=True)

#     return 'Video convertido a AVI en 1080p.'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



from flask import Flask, request
import subprocess
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Define un ThreadPoolExecutor para manejar múltiples subprocesos simultáneamente
executor = ThreadPoolExecutor(max_workers=20)  # Ajusta los workers según el servidor

def convert_video(input_video, output_video):
    command = ['ffmpeg', '-i', input_video, '-vf', 'scale=1920:1080', '-c:v', 'libx264', '-c:a', 'copy', output_video]
    # Usamos subprocess.Popen para permitir múltiples procesos
    process = subprocess.Popen(command)
    process.wait()  # Espera a que el proceso termine

@app.route('/convert', methods=['GET'])
def convert_video_endpoint():
    input_video = '/data/input_video.mp4'  # Cambia por tu video de entrada
    unique_id = uuid.uuid4()  # ID único para esta solicitud
    output_video = f'/data/output_video_{unique_id}.avi'  # Nombre de salida único

    # Ejecuta el proceso de conversión en un subproceso

