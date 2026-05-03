from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Inventory Service de AutoMex', version='1.0.0')

INVENTARIO = [
    {"auto_id": 1, "modelo": "Toyota Corolla", "stock": 8, "almacen": "CDMX", "estatus": "disponible"},
    {"auto_id": 2, "modelo": "Mazda CX-5", "stock": 5, "almacen": "Monterrey", "estatus": "disponible"},
    {"auto_id": 3, "modelo": "Nissan Sentra", "stock": 0, "almacen": "Guadalajara", "estatus": "agotado"},
    {"auto_id": 4, "modelo": "Honda Civic", "stock": 12, "almacen": "CDMX", "estatus": "disponible"},
    {"auto_id": 5, "modelo": "Volkswagen Jetta", "stock": 3, "almacen": "Puebla", "estatus": "bajo"},
]

@app.route('/')
def home():
    return jsonify({"servicio": "AutoMex Inventory Service", "version": "1.0.0", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/inventario')
def listar_inventario():
    return jsonify({"total_modelos": len(INVENTARIO), "inventario": INVENTARIO})

@app.route('/inventario/<int:auto_id>')
def stock_auto(auto_id):
    item = next((i for i in INVENTARIO if i["auto_id"] == auto_id), None)
    if item is None:
        return jsonify({"error": "Auto no encontrado en inventario"}), 404
    return jsonify(item)

@app.route('/inventario/almacen/<string:almacen>')
def stock_por_almacen(almacen):
    items = [i for i in INVENTARIO if i["almacen"].lower() == almacen.lower()]
    return jsonify({"almacen": almacen, "total": len(items), "items": items})

@app.route('/inventario/disponibles')
def disponibles():
    items = [i for i in INVENTARIO if i["estatus"] == "disponible"]
    return jsonify({"total": len(items), "items": items})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
