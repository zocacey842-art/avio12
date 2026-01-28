import eventlet
eventlet.monkey_patch()

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import hashlib
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aviator_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

game_state = {
    'phase': 'waiting',
    'countdown': 7,
    'multiplier': 1.00,
    'crash_point': 0,
    'start_time': None
}

def generate_crash_point():
    house_edge = 0.04
    instant_crash_chance = 0.01
    
    if random.random() < instant_crash_chance:
        return 1.00
    
    server_seed = hashlib.sha256(f"{random.random()}{time.time()}".encode()).hexdigest()
    client_seed = f"aviator_{random.random()}"
    combined = f"{server_seed}{client_seed}"
    hash_result = hashlib.sha256(combined.encode()).hexdigest()
    hash_int = int(hash_result[:13], 16)
    e = 2 ** 52
    
    result = (0.96 * ((100 * e - hash_int) / (e - hash_int))) / 100.0
    return max(1.00, round(result, 2))

def game_loop():
    while True:
        game_state['phase'] = 'countdown'
        game_state['countdown'] = 7
        game_state['multiplier'] = 1.00
        game_state['crash_point'] = generate_crash_point()
        
        for i in range(7, 0, -1):
            game_state['countdown'] = i
            socketio.emit('game_state', {
                'phase': 'countdown',
                'countdown': i,
                'multiplier': 1.00
            })
            eventlet.sleep(1)
        
        game_state['phase'] = 'running'
        game_state['start_time'] = time.time()
        
        socketio.emit('game_state', {
            'phase': 'running',
            'multiplier': 1.00
        })
        
        while True:
            elapsed = time.time() - game_state['start_time']
            multiplier = round(pow(2.71828, 0.05 * elapsed), 2)
            game_state['multiplier'] = multiplier
            
            socketio.emit('game_state', {
                'phase': 'running',
                'multiplier': multiplier
            })
            
            if multiplier >= game_state['crash_point']:
                break
            
            eventlet.sleep(0.05)
        
        game_state['phase'] = 'crashed'
        socketio.emit('game_state', {
            'phase': 'crashed',
            'multiplier': game_state['crash_point'],
            'crash_point': game_state['crash_point']
        })
        
        eventlet.sleep(3)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@socketio.on('connect')
def handle_connect():
    emit('game_state', {
        'phase': game_state['phase'],
        'countdown': game_state['countdown'],
        'multiplier': game_state['multiplier']
    })

@socketio.on('request_state')
def handle_request_state():
    emit('game_state', {
        'phase': game_state['phase'],
        'countdown': game_state['countdown'],
        'multiplier': game_state['multiplier']
    })

if __name__ == '__main__':
    socketio.start_background_task(game_loop)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
