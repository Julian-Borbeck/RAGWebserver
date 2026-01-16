from settings import settings
import requests

SYSTEM_PROMPT = """You are a RAG assistant answering questions about Multiple Sequence Alignment (MSA) with a focus on MAFFT, MUSCLE and CLUSTAL. Use the provided context to answer.
If the context is insufficient, say so in your message.
"""

def chat(query, context):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"QUESTION:\n{query}\n\nCONTEXT:\n{context}"},
    ]


    payload = {
        "model": settings.model_answer,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.6,
        }
    }

    r = requests.post(settings.model_url, json=payload, timeout=settings.timeout)
    r.raise_for_status()
    data = r.json()

    msg = data.get("message", {})
    content = msg.get("content", "")
    if not isinstance(content, str):
        content = str(content)
    return content.strip()