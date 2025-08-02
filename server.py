
import requests
import time

TICKETS_URL = 'https://www.realmadrid.com/es-ES/futbol/partidos/entradas/real-madrid-barcelona-26-10-2025'

KEY_LABELS = [
    'Próximamente a la venta',
    'La información de zonas y precios de aforo general aún no está disponible'
]

class ContentGetter:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            response.encoding = 'utf-8' # Set encoding to UTF-8 for Spanish accents
            return response.text
        except requests.RequestException as e:
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
    
if __name__ == "__main__":
    content_getter = ContentGetter(TICKETS_URL)
    print("Ticketing server started")

    while True:
        content = content_getter.get_content()

        if content is None:
            print("Failed to retrieve content.")
            time.sleep(30)  # Wait before retrying
            continue

        content_checker = ContentChecker(content, KEY_LABELS)
        missing_labels = content_checker.check_content()

        if len(missing_labels) > 0:
            print("TICKETING CHANGED - Labels:", ticketing_info)

            # TODO: Implement the logic to send a notification or alert
            exit(1)

        print("OK")
        time.sleep(30) # Wait for 30 seconds before the next check
