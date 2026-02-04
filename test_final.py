import requests
import json

url = "http://localhost:8000/api/v1/idea/full-plan"
data = {
    "skills": ["Python"],
    "interests": ["AI"],
    "experience_level": "beginner",
    "goal": "fun",
    "time_available": "1 week",
    "preferences": "test"
}
try:
    resp = requests.post(url, json=data)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("SUCCESS")
    else:
        print(f"ERROR: {resp.text}")
except Exception as e:
    print(f"FAILED: {e}")
