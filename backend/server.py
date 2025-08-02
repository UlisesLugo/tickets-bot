
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os

TICKETS_URL = 'https://www.realmadrid.com/es-ES/futbol/partidos/entradas/real-madrid-barcelona-26-10-2025'

KEY_LABELS = [
    'Próximamente a la venta',
    'La información de zonas y precios de aforo general aún no está disponible'
]

class ContentGetter:
    def __init__(self, requests, url):
        self.requests = requests
        self.url = url

    def get_content(self):
        try:
            response = self.requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            response.encoding = 'utf-8' # Set encoding to UTF-8 for Spanish accents
            return response.text
        except self.requests.RequestException as e:
            print(f"An error occurred while fetching the content: {e}")
            return None

class ContentChecker:
    def __init__(self, content, labels):
        self.content = content
        self.labels = labels

    def check_content(self):
        if self.content is None:
            return []

        missing_labels = []
        for i, label in enumerate(self.labels):
            if label not in self.content:
                missing_labels.append(i)
        return missing_labels
    
class NotificationSender:
    def __init__(self, requests, api_key):
        self.requests = requests
        self.api_key = api_key

    def send_notification(self):
        notification_name = "ticketBot" 

        url = f"https://api.pushcut.io/v1/notifications/{notification_name}"
        headers = {
            "API-Key": api_key
        }
        
        response = requests.post(url, headers=headers)
        print("NOTIFICATION Sent:", response.text)
    
if __name__ == "__main__":
    load_dotenv()
    print("Ticketing server started")

    api_key = os.getenv('API_KEY')
    if api_key is None:
        print("Error: API_KEY is not set in the environment variables.")
        exit(1)

    content_getter = ContentGetter(requests, TICKETS_URL)
    notification_sender = NotificationSender(requests, api_key)

    while True:
        content = content_getter.get_content()

        if content is None:
            print("Failed to retrieve content.")
            time.sleep(30)  # Wait before retrying
            continue

        content_checker = ContentChecker(content, KEY_LABELS)
        missing_labels = content_checker.check_content()

        if len(missing_labels) > 0:
            print("TICKETING CHANGED - Labels:", missing_labels)

            notification_sender.send_notification()
            exit(1)

        print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] OK")
        time.sleep(30) # Wait for 30 seconds before the next check
