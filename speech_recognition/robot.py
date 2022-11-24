import requests
import json

res = requests.get("http://localhost:5000/check")
print(json.loads(res.content.decode("utf-8")))