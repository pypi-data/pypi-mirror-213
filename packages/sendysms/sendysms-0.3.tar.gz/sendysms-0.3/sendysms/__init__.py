import requests

class Sendy:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = f"http://mailitant.ink/api/{api_key}"

    def send(self, phone, message):
        url = self.base_url
        payload = {"phone": phone, "message": message}
        response = requests.post(url, json=payload)
        return response

    def balance(self):
        url = self.base_url
        response = requests.get(url)
        return response
