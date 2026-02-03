from settings import settings
import requests

SYSTEM_PROMPT = """You are a RAG assistant answering questions about Multiple Sequence Alignment (MSA) with a focus on MAFFT, MUSCLE and CLUSTAL. Use the provided context to answer, reference the chunks you use for your answer by number.
If the context is insufficient, say so in your message.
"""

SYSTEM_PROMPT_NO_CONTEXT = """You are a RAG assistant answering questions about Multiple Sequence Alignment (MSA) with a focus on MAFFT, MUSCLE and CLUSTAL.
"""

SYSTEM_PROMPT_COMMAND = """You are a command generator for Multiple Sequence Alignment (MSA) tools with a focus on MAFFT, MUSCLE and CLUSTAL. Use the provided context to generate exactly one valid command (able to be executed in the shell without any processing), that adresses the user question for the tool you are asked for.
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

def chat_no_context(query):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_NO_CONTEXT},
        {"role": "user", "content": f"QUESTION:\n{query}"},
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

def chat_command(query, context):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_COMMAND},
        {"role": "user", "content": f"QUESTION:\n{query}\n\nCONTEXT:\n{context}"},
    ]


    payload = {
        "model": settings.model_answer,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.4,
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