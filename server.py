
import requests
import time

TICKETS_URL = 'https://www.realmadrid.com/es-ES/futbol/partidos/entradas/real-madrid-barcelona-26-10-2025'

KEY_LABELS = [
    'Próximamente a la venta',
    'La información de zonas y precios de aforo general aún no está disponible'
]

def check_ticketing_info(requests, url, labels):
    response = requests.get(url)

    # Set encoding to UTF-8 for Spanish accents
    response.encoding = 'utf-8'

    result = []
    for i, label in enumerate(labels):
        if label not in response.text:
            result.append(i)
    return result


print("Checking for key labels in the response...")

while True:
    try:

        ticketing_info = check_ticketing_info(requests, TICKETS_URL, KEY_LABELS)

        if not ticketing_info:
            print("All key labels found.")
        else:
            print("TICKETING CHANGED - Labels:", ticketing_info)
        
        time.sleep(30)  # Wait for 30 seconds before the next check

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        break