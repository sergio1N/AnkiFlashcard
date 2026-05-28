import requests
response = requests.post('http://localhost:8765', json={
    "action": "modelFieldNames",
    "version": 6,
    "params": { "modelName": "Básico" }
})
print(response.json())
