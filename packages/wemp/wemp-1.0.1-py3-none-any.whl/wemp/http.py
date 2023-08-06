import os
import requests
import traceback
from tqdm import tqdm
import json

def heart(url, token):
    try:
        response   = requests.post(url, json.dumps({"token": token}), headers={
            "Content-Type": "application/json; charset=UTF-8"
        })
        data = json.loads(str(response.content, encoding="utf-8"))
        if response.status_code != 200:
            print(f"Failed to request, {data['message']}")
            return None
        return data
    except Exception as e:
        print(f"Failed to request server.")
        return None

def update(url, token, message):
    try:
        response   = requests.post(url, data=json.dumps({"token": token, "message": message}), headers={
            "Content-Type": "application/json; charset=UTF-8",
        })
        data = json.loads(str(response.content, encoding="utf-8"))
        if response.status_code != 200:
            print(f"Failed to request, {data['message']}")
            return None
        return data
    except Exception as e:
        print(f"Failed to request server.")
        return None