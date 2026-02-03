# RAGWebserver
A webserver prototype RAG system for multiple sequence alignment built using streamlit.

## Installation
Please install the conda environment via conda env create -f environment.yml

The Webserver can then be started from the root directory using the command streamlit run app.py --server.adress=0.0.0.0 --server.port=8501

##Configuration
Configuration, such as the url and port for the retrieval service, LLM model service, the chroma DB directory, request timeout, rewrites and chunks to retrieve can be set in .env
