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

def retrieval_ab(query, n_rewrites, n_chunks):

    payload = {"query": query, "n_rewrites": n_rewrites, "n_chunks": n_chunks}
    r = requests.post(settings.ab_retrieval_url, json=payload, timeout=settings.timeout)
    r.raise_for_status()
    data = r.json()
    optionA = data[0]
    optionB = data[1]

    dataA = optionA.get("data", {})
    dataB = optionB.get("data", {})

    corpusA = optionA.get("corpus", "")
    corpusB = optionB.get("corpus", "")

    chunksA = dataA.get("chunks", [])
    chunksB = dataB.get("chunks", [])  # <-- FIXED
    metadataA = dataA.get("metadata", [])
    metadataB = dataB.get("metadata", [])

    if not isinstance(chunksA, list) or not isinstance(chunksB, list):
        raise ValueError("Retrieval response must contain 'chunks' as lists for both A and B.")
    if not isinstance(metadataA, list) or not isinstance(metadataB, list):
        raise ValueError("Retrieval response must contain 'metadata' as lists for both A and B.")
    
    return corpusA, chunksA, metadataA, corpusB, chunksB, metadataB