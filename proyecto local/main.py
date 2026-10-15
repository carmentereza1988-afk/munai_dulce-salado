import os 
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_local_secreto_123'
socketio = SocketIO(app, cors_allowed_origins="*")

pedidos = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('nuevo_pedido')
def handle_nuevo_pedido(data):
    nuevo_id = len(pedidos) + 1
    data['id'] = nuevo_id
    data['estado'] = 'Pendiente'
    pedidos.append(data)
    emit('recibir_pedido', data, broadcast=True)

@socketio.on('cambiar_estado')
def handle_cambiar_estado(data):
    pedido_id = data.get('id')
    nuevo_estado = data.get('estado')

    for p in pedidos:
        if p['id'] == pedido_id:
            p['estado'] = nuevo_estado
            break

    emit('actualizar_lista', pedidos, broadcast=True)
@app.route('/caja')
def caja():
    return render_template('caja.html')
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor corriendo en puerto {port}")
    socketio.run(app, host='0.0.0.0', port=port)
