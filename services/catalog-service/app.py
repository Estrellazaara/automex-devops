from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Catalog Service de AutoMex', version='1.0.0')

# Catálogo simulado de autos
CATALOGO = [
    {"id": 1, "marca": "Toyota", "modelo": "Corolla", "anio": 2024, "precio": 389000, "disponible": True},
    {"id": 2, "marca": "Mazda", "modelo": "CX-5", "anio": 2024, "precio": 525000, "disponible": True},
    {"id": 3, "marca": "Nissan", "modelo": "Sentra", "anio": 2024, "precio": 365000, "disponible": False},
    {"id": 4, "marca": "Honda", "modelo": "Civic", "anio": 2024, "precio": 449000, "disponible": True},
    {"id": 5, "marca": "Volkswagen", "modelo": "Jetta", "anio": 2024, "precio": 410000, "disponible": True},
]

@app.route('/')
def home():
    return jsonify({"servicio": "AutoMex Catalog Service", "version": "1.0.0", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/autos')
def listar_autos():
    return jsonify({"total": len(CATALOGO), "autos": CATALOGO})

@app.route('/autos/<int:auto_id>')
def detalle_auto(auto_id):
    auto = next((a for a in CATALOGO if a["id"] == auto_id), None)
    if auto is None:
        return jsonify({"error": "Auto no encontrado"}), 404
    return jsonify(auto)

@app.route('/autos/disponibles')
def autos_disponibles():
    disponibles = [a for a in CATALOGO if a["disponible"]]
    return jsonify({"total": len(disponibles), "autos": disponibles})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
