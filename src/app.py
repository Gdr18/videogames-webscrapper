from flask import Flask, render_template, request, jsonify, send_file
from config import CONFIG

from src.scraper import get_data
from src.app_requests import post_game_api
from src.json_maker import create_json_file
from src.platform_enum import PlatformScrapperEnum

def create_app(config: dict) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    return application

app = create_app(CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<int:page>', methods=['POST'])
def search(page):
    platform = request.form.get('platform', '')
    direction = request.form.get('direction', '')
    
    if (not platform) or (not platform.replace("-", "_").upper()):
        return render_template('index.html', error="Por favor selecciona una plataforma")
    
    page -= 1
    
    if direction:
        page += 1 if direction == 'next' else -1
    
    try:
        data = get_data(platform, page)
        if not data or len(data) == 0:
            raise ValueError("No hay datos")
        
        return render_template('results.html', platform=platform, data=data, page=page + 1)
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return render_template('index.html', error="Error al obtener los datos")

@app.route('/download', methods=['POST'])
def download_json():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para descargar"}), 400
    try:
        filepath, filename = create_json_file(data['data'])
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Error al crear el archivo JSON: {e}")
        return jsonify({"error": "Error al obtener el archivo JSON"}), 500

@app.route('/send-db', methods=['POST'])
def send_data():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para enviar"}), 400
    
    games = data['data']
    success_count = 0
    
    try:
        for game in games:
            result = post_game_api(game)
            if result:
                success_count += 1
        
        return jsonify({
            "success": True,
            "message": f"Se enviaron {success_count} registros a la base de datos"
        })
    except Exception as e:
        print(f"Error al enviar los datos a la API: {e}")
        return jsonify({"error": "Error al registrar los datos"}), 500
