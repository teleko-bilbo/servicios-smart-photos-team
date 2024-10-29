from flask import Flask, jsonify
import subprocess
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Define un ThreadPoolExecutor para manejar múltiples subprocesos simultáneamente
executor = ThreadPoolExecutor(max_workers=20)  # Ajusta los workers según el servidor

# Almacena los mensajes de estado de las conversiones
conversion_status = {}

def convert_video(input_video, output_video, unique_id):
    command = ['ffmpeg', '-i', input_video, '-vf', 'scale=1920:1080', '-c:v', 'libx264', '-c:a', 'copy', output_video]
    # Usamos subprocess.Popen para permitir múltiples procesos
    process = subprocess.Popen(command)
    process.wait()  # Espera a que el proceso termine

    # Al finalizar, guarda el mensaje de éxito en el diccionario
    conversion_status[unique_id] = f'Conversión de video completada, archivo de salida: {output_video}'

@app.route('/convert', methods=['GET'])
def convert_video_endpoint():
    input_video = '/data/input_video.mp4'  # Cambia por tu video de entrada
    unique_id = str(uuid.uuid4())  # ID único para esta solicitud
    output_video = f'/data/output_video_{unique_id}.avi'  # Nombre de salida único

    # Ejecuta el proceso de conversión en un hilo separado
    executor.submit(convert_video, input_video, output_video, unique_id)

    # Envía una respuesta inmediata indicando que la conversión ha comenzado
    return jsonify({'message': 'Conversión de video iniciada.', 'unique_id': unique_id})

@app.route('/status/<unique_id>', methods=['GET'])
def get_conversion_status(unique_id):
    # Devuelve el estado de la conversión
    message = conversion_status.get(unique_id, 'La conversión está en progreso.')
    return jsonify({'status': message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
