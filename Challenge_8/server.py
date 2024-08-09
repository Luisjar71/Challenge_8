from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'logs.db'

# Diccionario de tokens para cada servicio
tokens = {
    "Service1": "token_service1_ABC123",
    "Service2": "token_service2_DEF456",
    "Service3": "token_service3_GHI789"
}

def reset_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS logs')
        init_db()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                service_name TEXT,
                log_level TEXT,
                message TEXT
            )
        ''')
        conn.commit()

def check_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    # Extrae el token del encabezado Authorization
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
    
    # Verifica si el token es válido y corresponde a un servicio
    for service_name, service_token in tokens.items():
        if token == service_token:
            return service_name
    return None

@app.route('/logs', methods=['POST'])
def receive_logs():
    service_name = check_token(request)
    if not service_name:
        return jsonify({"error": "Unauthorized"}), 401


    log_data = request.get_json()
    if not log_data:
        return jsonify({"error": "No log data received"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (timestamp, service_name, log_level, message)
            VALUES (?, ?, ?, ?)
        ''', (log_data['timestamp'], log_data['service_name'], log_data['log_level'], log_data['message']))
        conn.commit()
    
    return jsonify({"message": "Log received"}), 200

if __name__ == "__main__":
    reset_db()
    app.run(port=5000)
