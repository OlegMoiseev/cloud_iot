import requests

data = {"latitude": 59.890493,
        "longitude": 30.289959}

r = requests.post("http://trash-system.herokuapp.com/add", json=data)
print(r.text)

# data = {"id": 1,
#         "fullness": 26}
# r = requests.post("http://0.0.0.0:5000/update", json=data)
# print(r.text)