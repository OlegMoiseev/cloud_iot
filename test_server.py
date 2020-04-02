import requests

# data = {"latitude": 12.345567,
#         "longitude": 43.231323}
#
# r = requests.post("http://127.0.0.1:5000/add", json=data)
# print(r.text)

data = {"id": 6,
        "fullness": 27}
r = requests.post("http://127.0.0.1:5000/update", json=data)
print(r.text)