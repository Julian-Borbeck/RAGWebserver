import requests
from settings import settings

def retrieval(query, n_rewrites, n_chunks):

    payload = {"query": query, "n_rewrites": n_rewrites, "n_chunks": n_chunks}
    r = requests.post(settings.retrieval_url, json=payload, timeout=settings.timeout)
    r.raise_for_status()
    data = r.json()
    chunks = data.get("chunks", [])
    metadata = data.get("metadata", [])
    if not isinstance(chunks, list) or not isinstance(metadata, list):
        raise ValueError("Retrieval response must contain 'chunks' and 'metadata' as lists.")
    return chunks, metadata