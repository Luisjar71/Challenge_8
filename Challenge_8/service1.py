import time
import json
import requests
import random
from datetime import datetime

# Configuración del servicio
SERVICE_NAME = "Service1"
API_ENDPOINT = "http://localhost:5000/logs"
TOKEN = "token_service1_ABC123"  # Token único para Service1

def generate_log():
    levels = ["INFO", "ERROR", "DEBUG", "WARNING", "CRITICAL"]
    messages = ["Operation successful", "An error occurred", "Debugging information", "A warning message", "Critical issue encountered"]

    while True:
        level = random.choice(levels)
        message = random.choice(messages)
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "service_name": SERVICE_NAME,
            "log_level": level,
            "message": message
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {TOKEN}"  # Incluye el token en el encabezado Authorization
        }
        try:
            response = requests.post(API_ENDPOINT, data=json.dumps(log_data), headers=headers)
            if response.status_code == 200:
                print(f"Log sent successfully from {SERVICE_NAME}: {log_data}")
            else:
                print(f"Failed to send log from {SERVICE_NAME}: {log_data}")
        except Exception as e:
            print(f"Error sending log from {SERVICE_NAME}: {e}")
        time.sleep(10)  # Generar un log cada 10 segundos

if __name__ == "__main__":
    generate_log()
