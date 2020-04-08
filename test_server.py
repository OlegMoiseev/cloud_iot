import requests

# data = {"latitude": 12.325567,
#         "longitude": 43.271323}
#
# r = requests.post("http://0.0.0.0:5000/add", json=data)
# print(r.text)

data = {"id": 1,
        "fullness": 26}
r = requests.post("http://0.0.0.0:5000/update", json=data)
print(r.text)