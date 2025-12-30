import requests
import json

def test_chat_endpoint():
    url = "http://localhost:8000/api/chat"

    payload = {
        "message": "What is embodied intelligence in humanoid robots?",
        "selected_text": None,
        "current_page": None
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing chat endpoint with RAG integration...")
    test_chat_endpoint()