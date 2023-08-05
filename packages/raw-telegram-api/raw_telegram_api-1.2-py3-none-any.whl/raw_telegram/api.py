import requests

class APIClient():
    def __init__(self, token):
        self.url = "https://api.telegram.org/bot" + token
        self.token = token
    def send_method(self, method, data):
        uri = self.url + "/" + method
        return requests.get(uri, params=data).content
    def __str__(self):
        return "APIClient instance with API token " + self.token
    def __repr__(self):
        return "APIClient instance with API token " + self.token
