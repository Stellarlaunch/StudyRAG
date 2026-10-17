import streamlit as st
from ask import answer, retrieve

st.set_page_config(page_title="StudyRAG", page_icon="📚", layout="centered")

EXAMPLES = [
    "What retriever does RAG use?",
    "What is the difference between the RAG-Sequence and RAG-Token models?",
    "Which optimizer is used to train the model?",
    "How many trainable parameters do the RAG models have in total?",
]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None

with st.sidebar:
    st.title("📚 StudyRAG")
    st.write(
        "Ask questions about the paper *Retrieval-Augmented Generation "
        "for Knowledge-Intensive NLP Tasks*. Answers come only from retrieved "
        "chunks and cite page numbers."
    )
    st.divider()
    st.subheader("Try an example")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
    st.divider()
    st.caption("Search: all-MiniLM-L6-v2 + ChromaDB, 400-char chunks, top 5")
    st.caption("Retrieval hit rate: 14/15 on a 15-question eval set")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("StudyRAG")
st.caption("Ask a question. Get an answer with page citations.")


def render_assistant(msg):
    st.markdown(msg["text"])
    st.caption("Pages searched: " + ", ".join(f"p.{p}" for p in msg["pages"]))
    with st.expander("Show retrieved chunks"):
        for doc, meta in msg["chunks"]:
            st.markdown(f"**Page {meta['page']}**")
            st.text(doc)


if not st.session_state.messages:
    st.info("Pick an example from the sidebar or type your own question below.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "user":
            st.markdown(m["text"])
        else:
            render_assistant(m)

typed = st.chat_input("Ask about the paper...")
question = typed or st.session_state.pending
st.session_state.pending = None

if question:
    st.session_state.messages.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the paper..."):
            try:
                text, pages = answer(question)
                chunks = retrieve(question)
                msg = {"role": "assistant", "text": text, "pages": pages, "chunks": chunks}
                render_assistant(msg)
                st.session_state.messages.append(msg)
            except Exception as e:
                st.error(
                    "Something went wrong while generating the answer. On the free "
                    "Gemini tier this is often a rate limit, so wait a minute and try again."
                )
                st.caption(str(e)[:200])