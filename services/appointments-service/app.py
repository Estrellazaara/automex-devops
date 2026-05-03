from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Appointments Service de AutoMex', version='1.0.0')

CITAS = [
    {"id": 1, "cliente": "María Pérez", "auto_id": 1, "fecha": "2026-05-05 10:00", "estado": "confirmada"},
    {"id": 2, "cliente": "Juan López", "auto_id": 2, "fecha": "2026-05-05 12:00", "estado": "confirmada"},
    {"id": 3, "cliente": "Ana García", "auto_id": 4, "fecha": "2026-05-06 16:00", "estado": "pendiente"},
]

@app.route('/')
def home():
    return jsonify({"servicio": "AutoMex Appointments Service", "version": "1.0.0", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/citas')
def listar_citas():
    return jsonify({"total": len(CITAS), "citas": CITAS})

@app.route('/citas/<int:cita_id>')
def detalle_cita(cita_id):
    cita = next((c for c in CITAS if c["id"] == cita_id), None)
    if cita is None:
        return jsonify({"error": "Cita no encontrada"}), 404
    return jsonify(cita)

@app.route('/citas', methods=['POST'])
def crear_cita():
    data = request.get_json()
    if not data or "cliente" not in data or "auto_id" not in data or "fecha" not in data:
        return jsonify({"error": "Faltan campos: cliente, auto_id, fecha"}), 400
    nueva_cita = {
        "id": len(CITAS) + 1,
        "cliente": data["cliente"],
        "auto_id": data["auto_id"],
        "fecha": data["fecha"],
        "estado": "pendiente"
    }
    CITAS.append(nueva_cita)
    return jsonify(nueva_cita), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
