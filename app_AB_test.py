import streamlit as st
import uuid
import random
import hashlib

from settings import settings
from service_adapters.chat import chat, chat_no_context
from service_adapters.retrieval import retrieval_ab
from util.util import format_context, log_event

def stable_shuffle_key(question: str, session_id: str) -> int:
    s = (session_id + "::" + question).encode("utf-8")
    return int(hashlib.sha256(s).hexdigest(), 16)

st.set_page_config(page_title="MSA RAG (Paired Test)", layout="wide")
st.title("Multiple Sequence Alignment RAG (Paired Comparison)")

n_rewrites = int(getattr(settings, "n_rewrites", 2))
n_chunks = int(getattr(settings, "n_chunks", 8))

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
session_id = st.session_state["session_id"]

main = st.container()

with st.sidebar:
    st.header("Report preference")
    st.caption("Submit a question first, then pick the better answer here.")

    pair_state = st.session_state.get("pair_state")
    if not pair_state:
        st.info("No answers yet.")
    else:
        pref_key = f"pref_choice::{pair_state['session_id']}::{stable_shuffle_key(pair_state['question'], pair_state['session_id'])}"
        reason_key = f"pref_reason::{pair_state['session_id']}::{stable_shuffle_key(pair_state['question'], pair_state['session_id'])}"

        choice = st.radio(
            "Which is better?",
            options=["Answer 1", "Answer 2", "Tie"],
            index=None,
            key=pref_key,
        )
        reason = st.text_area("Optional: why?", height=110, key=reason_key)

        submit_pref = st.button("Submit preference", disabled=(choice is None))
        if submit_pref:
            items = pair_state["items"]

            winner_variant = None
            winner_corpus = None
            if choice == "Answer 1":
                winner_variant = items[0]["variant"]
                winner_corpus = items[0]["corpus"]
            elif choice == "Answer 2":
                winner_variant = items[1]["variant"]
                winner_corpus = items[1]["corpus"]

            log_event(
                {
                    "event": "paired_preference",
                    "session_id": pair_state["session_id"],
                    "question": pair_state["question"],
                    "winner": winner_variant,
                    "winner_corpus": winner_corpus,
                    "presented": [
                        {"slot": 1, "variant": items[0]["variant"], "corpus": items[0]["corpus"]},
                        {"slot": 2, "variant": items[1]["variant"], "corpus": items[1]["corpus"]},
                    ],
                    "reason": reason,
                    "n_rewrites": pair_state["n_rewrites"],
                    "n_chunks": pair_state["n_chunks"],
                }
            )

            st.success("Preference recorded.")
            st.rerun()

with main:
    question = st.text_area(
        "Ask a question about Multiple Sequence Alignments",
        value="",
        height=110,
        placeholder="Type your question here...",
    )
    ask = st.button("Submit", type="primary", disabled=(not question.strip()))

    if ask:
        q = question.strip()
        st.session_state.pop("pair_state", None)

        try:
            with st.status("Retrieving chunks (A and B)...", expanded=False):
                corpusA, chunksA, metadataA, corpusB, chunksB, metadataB = retrieval_ab(q, n_rewrites, n_chunks)

                if not chunksA and not chunksB:
                    st.warning("No chunks found in either variant.")
                    st.stop()

                contextA = format_context(chunksA, metadataA) if chunksA else None
                contextB = format_context(chunksB, metadataB) if chunksB else None

            with st.status("Calling model twice (A and B)...", expanded=True):
                answerA = chat(q, contextA) if contextA else chat_no_context(q)
                answerB = chat(q, contextB) if contextB else chat_no_context(q)

            rng = random.Random(stable_shuffle_key(q, session_id))
            pair = [
                {"label": "Answer 1", "variant": "A", "corpus": corpusA, "answer": answerA},
                {"label": "Answer 2", "variant": "B", "corpus": corpusB, "answer": answerB},
            ]
            rng.shuffle(pair)

            st.session_state["pair_state"] = {
                "question": q,
                "session_id": session_id,
                "items": pair,
                "n_rewrites": n_rewrites,
                "n_chunks": n_chunks,
            }

            st.rerun()

        except Exception as e:
            st.exception(e)

    pair_state = st.session_state.get("pair_state")
    if pair_state:
        items = pair_state["items"]
        a, b = st.columns(2, gap="large")

        with a:
            st.subheader(items[0]["label"])
            st.markdown(items[0]["answer"])

        with b:
            st.subheader(items[1]["label"])
            st.markdown(items[1]["answer"])
    else:
        st.caption("Submit a question to see two answers side by side.")
