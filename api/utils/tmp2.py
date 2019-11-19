import requests

url = 'https://im.hygtchat.com:15001/robot/api/incoming/message/c8ba5153e3124887b5c9cb0a4cf4b9bc'
data = {
    "group": "%s" % '11627',
    "title": 'test',
    "text": 'this is a test.',
}

requests.post(url, timeout=5, json=data, headers={'Content-Type': 'application/json'}, verify=False)