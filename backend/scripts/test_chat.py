import requests

url = "http://127.0.0.1:8000/chat/"
json_data = {"query": "hello", "session_id": "test123"}
resp = requests.post(url, json=json_data)
print(resp.status_code)
print(resp.text)
