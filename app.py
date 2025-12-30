from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime

from scrapper import get_data
from send_videogames import post_games

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<int:page>', methods=['POST'])
def search(page):
    platform = request.form.get('platform', '') or request.json.get('platform', '')
    
    if not platform:
        return render_template('index.html', error="Por favor selecciona una plataforma")
    
    data = get_data(platform, page)
    
    return render_template('results.html', platform=platform, data=data, page=page)

@app.route('/download', methods=['POST'])
def download_json():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para descargar"}), 400
    
    filename = f"videogames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join('temp', filename)
    
    os.makedirs('temp', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data['data'], f, ensure_ascii=False, indent=2)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/send-db', methods=['POST'])
def send_data():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para enviar"}), 400
    

    try:
        registers_count = post_games(data['data'])
        
        return jsonify({
            "success": True,
            "message": f"Se enviaron {registers_count} registros a la base de data"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

