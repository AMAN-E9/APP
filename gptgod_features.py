import requests

API_KEY = "sk-OsMMq65tXdfOIlTUYtocSL7NCsmA7CerN77OkEv29dODg1EA"
BASE_URL = "https://api.gptgod.online"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chat_with_gptgod(prompt, model="net-gpt-3.5-turbo"):
    url = f"{BASE_URL}/v1/chat/completions"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }
    res = requests.post(url, headers=HEADERS, json=data)
    if res.status_code == 200:
        return res.json()['choices'][0]['message']['content']
    return f"❌ Error: {res.status_code} - {res.text}"

def generate_image(prompt, size="512x512"):
    url = f"{BASE_URL}/v1/images/generations"
    data = {
        "model": "stable-diffusion",
        "prompt": prompt,
        "n": 1,
        "size": size
    }
    res = requests.post(url, headers=HEADERS, json=data)
    if res.status_code == 200:
        return res.json()['data'][0]['url']
    return f"❌ Error: {res.status_code} - {res.text}"
