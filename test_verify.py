import urllib.request
import json

def test_plan_generation():
    url = "http://localhost:8000/api/v1/idea/full-plan"
    payload = {
        "skills": ["Python", "JavaScript"],
        "interests": ["Web Development"],
        "experience_level": "intermediate",
        "goal": "portfolio",
        "time_available": "1 Months",
        "preferences": ""
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    print(f"Testing POST {url}...")
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            print(f"Status: {status}")
            if status == 200:
                print("SUCCESS: Plan generated!")
                result = json.loads(response.read().decode('utf-8'))
                print(f"Project Title: {result['idea']['title']}")
            else:
                print(f"FAILED: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_plan_generation()
