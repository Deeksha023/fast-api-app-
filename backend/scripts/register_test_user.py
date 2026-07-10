import urllib.request, json

data = {
    "email": "swagger@example.com",
    "password": "secret",
    "role": "Candidate",
    "name": "Swagger"
}

url = 'http://localhost:8000/auth/register'
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.status)
        print(resp.read().decode())
except Exception as e:
    import traceback
    traceback.print_exc()
    if hasattr(e, 'read'):
        try:
            print(e.read().decode())
        except Exception:
            pass
