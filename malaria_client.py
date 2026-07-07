import streamlit as st
import malaria_rag


def prepare_streamlit_display(response: dict) -> dict:
    """Format backend results for a Streamlit chat-style display."""
    sources = response.get("sources", []) or []
    snippets = response.get("snippets", []) or []

    citations = []
    for index, source in enumerate(sources):
        citations.append({
            "id": source.get("id") or (index + 1),
            "citation": source.get("citation") or source.get("document") or f"Document {index + 1}",
            "snippet": snippets[index] if index < len(snippets) else None,
        })

    return {
        "answer": response.get("answer", ""),
        "citations": citations,
        "latency_ms": response.get("latency_ms"),
    }


st.set_page_config(page_title="MalariaAI RAG", page_icon="🦟", layout="wide")
st.title("🦟 MalariaAI RAG")
st.caption("Ask questions about malaria policies and review the separate citations below each answer.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("citations"):
            with st.expander("Citations"):
                for citation in message["citations"]:
                    st.markdown(f"**[{citation['id']}] {citation['citation']}**")
                    if citation.get("snippet"):
                        st.caption(citation["snippet"])

if prompt := st.chat_input("Ask about malaria policies..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "citations": []})

    response = malaria_rag.answer_and_sources(question=prompt)
    display = prepare_streamlit_display(response)

    with st.chat_message("assistant"):
        st.markdown(display["answer"])
        if display["citations"]:
            with st.expander("Citations"):
                for citation in display["citations"]:
                    st.markdown(f"**[{citation['id']}] {citation['citation']}**")
                    if citation.get("snippet"):
                        st.caption(citation["snippet"])
        if display.get("latency_ms") is not None:
            st.caption(f"Latency: {display['latency_ms']} ms")

    st.session_state.messages.append({
        "role": "assistant",
        "content": display["answer"],
        "citations": display["citations"],
        "latency_ms": display.get("latency_ms"),
    })
