import requests

url = "http://127.0.0.1:5000/analyze-document"

headers = {
    "x-api-key": "12345"
}

files = {
    "file": open("sample-1.pdf", "rb")
}

response = requests.post(url, headers=headers, files=files)

print(response.json())