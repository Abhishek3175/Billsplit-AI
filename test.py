import requests

API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/llama-4-maverick:free",  # simple text test
    "messages": [
        {"role": "user", "content": "Say hello in JSON format with a field greeting"}
    ]
}

response = requests.post(URL, headers=headers, json=data)
print(response.json())
