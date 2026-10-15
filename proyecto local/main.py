import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'munai_secreto_2026'

# Lista en memoria para los pedidos
pedidos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caja')
def caja():
    return render_template('caja.html')

# API GET: La caja lee los pedidos aquí
@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    return jsonify(pedidos)

# API POST: El cliente o la caja envían un pedido nuevo aquí
@app.route('/api/pedidos', methods=['POST'])
def guardar_pedido():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Sin datos'}), 400
    
    nuevo_id = len(pedidos) + 1
    data['id'] = nuevo_id
    if 'estado' not in data or not data['estado']:
        data['estado'] = 'Pendiente'
        
    pedidos.append(data)
    return jsonify({'status': 'ok', 'pedido': data})

# API POST: Cambiar estado (Pendiente -> Preparando -> Listo)
@app.route('/api/pedidos/estado', methods=['POST'])
def cambiar_estado():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error'}), 400
        
    pedido_id = data.get('id')
    nuevo_estado = data.get('estado')

    for p in pedidos:
        if p['id'] == pedido_id:
            p['estado'] = nuevo_estado
            break

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
