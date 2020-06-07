import requests

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json",
    "X-JNAP-Action": "http://cisco.com/jnap/router/GetWANStatus",
}

r = requests.post('http://192.168.1.1/JNAP/', headers=headers, data='{}', verify=False)
data = r.json()
print(data)
