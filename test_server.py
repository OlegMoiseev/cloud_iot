import requests

data = {"latitude": 59.879088,
        "longitude": 29.913754}

r = requests.post("http://trash-system.herokuapp.com/add", json=data)
print(r.text)

# data = {"id": 1,
#         "fullness": 26}
# r = requests.post("http://0.0.0.0:5000/update", json=data)
# print(r.text)