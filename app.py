from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

# Datos de ejemplo para el JSON (puedes reemplazarlos con tus datos reales)
SAMPLE_DATA = {
    "ps5": [
        {"id": 1, "nombre": "God of War Ragnarök", "precio": 69.99, "plataforma": "PS5"},
        {"id": 2, "nombre": "Horizon Forbidden West", "precio": 59.99, "plataforma": "PS5"},
        {"id": 3, "nombre": "Spider-Man 2", "precio": 69.99, "plataforma": "PS5"},
        {"id": 1, "nombre": "God of War Ragnarök", "precio": 69.99, "plataforma": "PS5"},
        {"id": 2, "nombre": "Horizon Forbidden West", "precio": 59.99, "plataforma": "PS5"},
        {"id": 3, "nombre": "Spider-Man 2", "precio": 69.99, "plataforma": "PS5"}
    ],
    "xbox": [
        {"id": 1, "nombre": "Halo Infinite", "precio": 59.99, "plataforma": "Xbox"},
        {"id": 2, "nombre": "Forza Horizon 5", "precio": 59.99, "plataforma": "Xbox"},
        {"id": 3, "nombre": "Starfield", "precio": 69.99, "plataforma": "Xbox"},
        {"id": 1, "nombre": "Halo Infinite", "precio": 59.99, "plataforma": "Xbox"},
        {"id": 2, "nombre": "Forza Horizon 5", "precio": 59.99, "plataforma": "Xbox"},
        {"id": 3, "nombre": "Starfield", "precio": 69.99, "plataforma": "Xbox"}
    ],
    "pc": [
        {"id": 1, "nombre": "Baldur's Gate 3", "precio": 59.99, "plataforma": "PC"},
        {"id": 1, "nombre": "Baldur's Gate 3", "precio": 59.99, "plataforma": "PC"},
        {"id": 1, "nombre": "Baldur's Gate 3", "precio": 59.99, "plataforma": "PC"},
        {"id": 2, "nombre": "Cyberpunk 2077", "precio": 49.99, "plataforma": "PC"},
        {"id": 3, "nombre": "Elden Ring", "precio": 59.99, "plataforma": "PC"},
        {"id": 3, "nombre": "Elden Ring", "precio": 59.99, "plataforma": "PC"}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<int:page>', methods=['POST'])
def search(page):
    platform = request.form.get('platform', '') or request.json.get('platform', '')
    
    if not platform:
        return render_template('index.html', error="Por favor selecciona una plataforma")
    
    # Obtener datos según la platform seleccionada
    data = SAMPLE_DATA.get(platform, [])
    
    return render_template('results.html', platform=platform, data=data, page=page)

@app.route('/download', methods=['POST'])
def download_json():
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para descargar"}), 400
    
    filename = f"videogames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join('temp', filename)
    
    os.makedirs('temp', exist_ok=True)
    
    # Guardar JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data['data'], f, ensure_ascii=False, indent=2)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/send-db', methods=['POST'])
def send_data():
    """Envía los data a la base de data"""
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({"error": "No hay datos para enviar"}), 400
    
    # Aquí iría la lógica para insertar en la base de data
    # Por ahora solo simulamos el envío
    try:
        # TODO: Implementar inserción en base de datos
        # Ejemplo: insertar_data(data['data'])
        
        return jsonify({
            "success": True,
            "message": f"Se enviaron {len(data['data'])} registros a la base de data"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

