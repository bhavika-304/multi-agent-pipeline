from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def call_llm(messages: list, system_prompt: str = "") -> str:

    all_messages = []

    if system_prompt:

        all_messages.append({
            "role": "system",
            "content": system_prompt
        })

    all_messages.extend(messages)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=all_messages,
        max_tokens=2048,
        temperature=0.1,
    )

    return response.choices[0].message.content