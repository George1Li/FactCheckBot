import requests
import json

models = ["deepseek-r1:latest", "gemma3:12b"]
def to_ollama(text, type):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": models[type],
        "prompt": f"{text}"
    }

    response = requests.post(url, json=payload, stream=True)

    # Ollama отдаёт ответ по кускам (streaming), поэтому читаем построчно
    full_text = ""
    i = 0
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                # печатаем кусок
                print(data["response"], end="", flush=True)
                full_text += data["response"]

    return full_text

