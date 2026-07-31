import json
import urllib.request
import urllib.error
from urllib.parse import urlencode

# Login para obter o refresh original
login_data = urlencode({'username': 'testuser', 'password': 'Test1234!'}).encode()
login_req = urllib.request.Request('http://localhost:8000/api/auth/login/', data=login_data, method='POST')
login_req.add_header('Content-Type', 'application/x-www-form-urlencoded')

with urllib.request.urlopen(login_req) as resp:
    body = json.loads(resp.read().decode())
    old_refresh = body['refresh']

# Primeiro refresh para rotacionar o token
payload = json.dumps({'refresh': old_refresh}).encode()
refresh_req = urllib.request.Request('http://localhost:8000/api/auth/refresh/', data=payload, method='POST')
refresh_req.add_header('Content-Type', 'application/json')

with urllib.request.urlopen(refresh_req) as resp2:
    print('first_refresh_status', resp2.status)

# Reuso do refresh original após rotação
payload2 = json.dumps({'refresh': old_refresh}).encode()
refresh_req2 = urllib.request.Request('http://localhost:8000/api/auth/refresh/', data=payload2, method='POST')
refresh_req2.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(refresh_req2) as resp3:
        print(resp3.status)
        print(resp3.read().decode())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read().decode())
