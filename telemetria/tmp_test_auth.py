import json
import urllib.request
import urllib.error
from urllib.parse import urlencode

login_data = urlencode({'username': 'testuser', 'password': 'Test1234!'}).encode()
login_req = urllib.request.Request('http://localhost:8000/api/auth/login/', data=login_data, method='POST')
login_req.add_header('Content-Type', 'application/x-www-form-urlencoded')

with urllib.request.urlopen(login_req) as resp:
    body = json.loads(resp.read().decode())
    token = body['access']

payload = json.dumps({
    'veiculo_id': 1,
    'medicoes': [{
        'id_veiculo': 1,
        'temperatura': 85.5,
        'vibracao': 3.2,
        'rpm': 2500,
        'timestamp_coleta': '2026-04-16T10:30:00Z'
    }]
}).encode()

req2 = urllib.request.Request('http://localhost:8000/api/sync/offline/', data=payload, method='POST')
req2.add_header('Content-Type', 'application/json')
req2.add_header('Authorization', f'Bearer {token}')

try:
    with urllib.request.urlopen(req2) as resp2:
        print(resp2.status)
        print(resp2.read().decode())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read().decode())
