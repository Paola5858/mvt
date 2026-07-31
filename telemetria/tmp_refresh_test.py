import json
import urllib.request
from urllib.parse import urlencode

# Login para obter refresh token
login_data = urlencode({'username': 'testuser', 'password': 'Test1234!'}).encode()
login_req = urllib.request.Request('http://localhost:8000/api/auth/login/', data=login_data, method='POST')
login_req.add_header('Content-Type', 'application/x-www-form-urlencoded')

with urllib.request.urlopen(login_req) as resp:
    body = json.loads(resp.read().decode())
    refresh = body['refresh']

# Refresh token
payload = json.dumps({'refresh': refresh}).encode()
refresh_req = urllib.request.Request('http://localhost:8000/api/auth/refresh/', data=payload, method='POST')
refresh_req.add_header('Content-Type', 'application/json')

with urllib.request.urlopen(refresh_req) as resp2:
    print(resp2.status)
    print(resp2.read().decode())
