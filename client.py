import requests
import time
import logging

class TranslationClient:
    def __init__(self, base_url, max_retries=5):
        self.base_url = base_url
        self.max_retries = max_retries

    def get_status(self):
        url = f"{self.base_url}/status"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get('result')
        except requests.RequestException as e:
            logging.error(f"Error getting status: {e}")
            return "error"

    def poll_status(self, backoff_factor=2, initial_delay=1):
        retries = 0
        delay = initial_delay

        while retries < self.max_retries:
            result = self.get_status()

            if result == "completed" or result == "error":
                return result

            # Log and apply exponential backoff
            logging.info(f"Status: {result}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= backoff_factor
            retries += 1

        return "error"  # If retries exceeded

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = TranslationClient("http://127.0.0.1:5000")
    final_status = client.poll_status()
    logging.info(f"Final status: {final_status}")
