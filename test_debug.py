import requests
import json
import sys

url = "http://localhost:8000/api/v1/idea/full-plan"
headers = {"Content-Type": "application/json"}
data = {
    "skills": ["Python", "React"],
    "interests": ["AI"],
    "experience_level": "intermediate",
    "goal": "portfolio",
    "time_available": "2 months",
    "preferences": "Debug mode"
}

print(f"POST {url}")
try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        try:
            detail = response.json().get('detail', 'No detail found')
            print(f"ERROR DETAIL: {detail}")
        except:
            print(f"RAW RESP: {response.text}")
    else:
        print(f"SUCCESS")
except Exception as e:
    print(f"Connection Failed: {e}")
