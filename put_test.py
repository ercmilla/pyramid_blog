import requests
import json

payload = {'title': 'put test', 'body': 'put test body'}
headers = {'content-type': 'application/json'}
r = requests.put("http://localhost:6543/blog/4", data=json.dumps(payload), headers=headers)

print(r.text)
