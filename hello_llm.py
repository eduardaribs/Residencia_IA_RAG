import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega o arquivo .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL"),
    messages=[
        {
            "role": "user",
            "content": "Qual é a capital do Brasil?"
        }
    ]
)

print(response.choices[0].message.content)