"""Creates a request to the server hosted at 127.0.0.1:8893"""
import requests
import xmltodict

headers = {"Accept": "application/xml"}
for _ in range(1):
    response = requests.get("http://127.0.0.1:8893/environment", headers=headers)
    mime_type = response.headers.get("Content-Type")
    print("MIME Type:", mime_type)
    dict_data = xmltodict.parse(response.content)
    print(dict_data)
for _ in range(5):
    response = requests.get("http://127.0.0.1:8893/environment")
    print(response.status_code)
