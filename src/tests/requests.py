from urllib import response
from httpx import head
import httpx
import requests

url = "http://127.0.0.1:7771/login"

payload =  {
    "username":"hhh",
    "password_hash":"hhh"
}
headers = {
    "Content-Type":"application/json"
}

res = httpx.post(url, json=payload, headers=headers)

print(res.json())