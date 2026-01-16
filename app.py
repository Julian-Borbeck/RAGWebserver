from settings import settings
import streamlit as st
from service_adapters.retrieval import retrieval
from service_adapters.chat import chat
from util.util import format_context, validate_response_schema

st.set_page_config(page_title="MSA RAG", layout="wide")
st.title("Multiple Sequence Alignment RAG")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    question = st.text_area("Ask a question about Multiple Sequence Alignments", value="", height=110, placeholder="Type your question here...")

with col2:
    n_rewrites = st.slider("n_rewrites", min_value=0, max_value=10, value=settings.default_rewrites, step=1)
    n_chunks = st.slider("n_chunks", min_value=1, max_value=30, value=settings.default_chunks, step=1)
    show_metadata = st.checkbox("Show metadata", value=False)

ask = st.button("Submit", type="primary", disabled=(not question.strip()))

if ask:
    try:
        with st.status("Retrieving chunks...", expanded=False):
            chunks, metadata = retrieval(question.strip(), n_rewrites, n_chunks)
            if not chunks:
                st.warning("No chunks found.")
                st.stop()

            context = format_context(chunks, metadata)

            st.subheader("Retrieved context")
            for i, chunk in enumerate(chunks):
                st.markdown(f"**Chunk [{i}]**")
                st.write(chunk)

            if show_metadata:
                st.subheader("Chunk metadata")
                for i, md in enumerate(metadata):
                    st.markdown(f"**Metadata [{i}]**")
                    st.json(md)

        with st.status("Calling Model...", expanded=True):
            raw = chat(question.strip(), context)

            st.subheader("LLM output")
            st.markdown(raw)

    except Exception as e:
        st.exception(e)