import requests
for _ in range(100):
    response = requests.get('http://127.0.0.1:8893/hello')
    print(f"Status code: {response.status_code}")