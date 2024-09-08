import requests
import json
import os

def get_path(_path):
    return os.path.join(os.path.dirname(__file__), _path)


# Инициализируем переменную для хранения текста
transcription_text = ""

# Проходимся по каждому параграфу и добавляем его в переменную
with open(get_path('../final_texts/final_transcription.txt'), 'r') as tr_file:
    transcription_text = tr_file.read()

IAM_KEY = ''

with open(get_path('../IAM_TOKEN.txt'), 'r') as token_file:
    IAM_KEY = token_file.read()
IAM_KEY = IAM_KEY[:-1]    

def get_answer(role_text, official_flag):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': 'Bearer ' + IAM_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.07,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": role_text
            },
            {
                "role": "user",
                "text": transcription_text
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    final = response.json()['result']['alternatives'][0]['message']['text']
    with open(get_path('official_answer.json') if official_flag else 'unofficial_answer.json', 'w', encoding='utf-8') as file:
        file.write(final)

    
    
def generate(official_flag):
    role_text = ''
    with open(get_path("official_prompt.txt") if official_flag else get_path("unofficial_prompt.txt") , 'r') as text_file:
        role_text = text_file.read()
    get_answer(role_text, official_flag)
    
    



generate(0)
generate(1)
