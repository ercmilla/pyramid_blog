import requests
import json

payload = {'title': 'post test', 'body': 'post test body'}
headers = {'content-type': 'application/json'}
r = requests.post("http://localhost:6543/", data=json.dumps(payload), headers=headers)

print(r.text)
