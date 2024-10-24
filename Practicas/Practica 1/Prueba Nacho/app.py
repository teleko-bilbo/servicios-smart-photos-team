from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Ruta temporal para almacenar los videos subidos dentro del contenedor
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/encode', methods=['POST'])
def encode_video():
    try:
        # Verifica si se ha enviado un archivo en la petición
        if 'video_file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        # Obtiene el archivo del formulario
        video_file = request.files['video_file']
        
        # Verifica que el archivo tenga un nombre
        if video_file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        # Guarda el archivo en el contenedor
        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(input_file_path)
        
        # Obtiene el formato de salida desde el formulario
        output_format = request.form['output_format']
        if not output_format:
            return jsonify({'status': 'error', 'message': 'No output format specified'}), 400
        
        # Define el nombre y la ruta del archivo de salida
        output_file_name = f"output.{output_format}"
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file_name)
        
        # Construye el comando de FFmpeg para convertir el video
        command = ['ffmpeg', '-i', input_file_path, output_file_path]
        
        # Ejecuta el comando de FFmpeg
        subprocess.run(command, check=True)
        
        # Copia el archivo de salida al directorio original del archivo en la máquina host
        original_file_dir = os.path.dirname(input_file_path)  # Mantiene la carpeta original
        host_output_path = os.path.join(original_file_dir, output_file_name)
        
        # Devuelve el archivo convertido al directorio original del host
        if os.path.exists(output_file_path):
            os.rename(output_file_path, host_output_path)
        
        return jsonify({'status': 'success', 'output_file': host_output_path})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

