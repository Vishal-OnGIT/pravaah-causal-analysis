import streamlit as st
st.markdown("""
<style>
/* Page background */
.main {
    background-color: #f9fafb;
}

/* Title */
h1, h2, h3 {
    color: #1f2937;
}

/* Input box */
div[data-baseweb="input"] input {
    border-radius: 10px;
    border: 1px solid #6366f1;
}

/* Explanation box */
.explanation-box {
    background-color: #eef2ff;
    padding: 16px;
    border-left: 6px solid #6366f1;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Evidence cards */
.evidence-box {
    background-color: #ffffff;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 12px;
}

/* Transcript ID badge */
.transcript-badge {
    background-color: #dcfce7;
    color: #166534;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
}

/* Bullet text */
.evidence-text {
    color: #374151;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

from data_loader import load_conversations
from causal_engine import extract_causal_evidence, generate_explanation

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Causal Analysis of Escalated Conversations",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown("## 🧠 Causal Analysis of Escalated Conversations")
st.markdown(
    "Ask **WHY** customer conversations escalate — and see **evidence from real dialogue**."
)

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.header("🧭 Query Assistant")

example_queries = [
    "Why do customer conversations escalate?",
    "Why do repeated service failures escalate?",
    "Why do customers ask for supervisors?",
    "Why do customers threaten legal action?",
    "Why do long delays cause escalation?"
]

selected_example = st.sidebar.selectbox(
    "Try an example question",
    [""] + example_queries
)

st.sidebar.markdown("### ℹ️ How this works")
st.sidebar.markdown(
    "- Analyzes escalated conversations\n"
    "- Identifies causal dialogue patterns\n"
    "- Shows exact evidence from transcripts"
)

# ---------- MAIN QUERY INPUT ----------
query = st.text_input(
    "🔍 Ask a question",
    value=selected_example if selected_example else
    "Why do repeated service failures escalate?"
)

# ---------- QUERY BLOCK ----------
if query:
    df = load_conversations("Conversational_Transcript_Dataset.json")
    evidence, lenses = extract_causal_evidence(df, query)
    explanation = generate_explanation(lenses)

    st.divider()

    # ---------- CAUSAL EXPLANATION ----------
    st.subheader("📌 Causal Explanation")
    st.markdown(
        f"<div class='explanation-box'>{explanation}</div>",
        unsafe_allow_html=True
    )


    # ---------- CAUSAL FACTORS ----------
    if lenses:
        st.markdown("**Identified Causal Factors:**")
        cols = st.columns(len(lenses))
        for i, lens in enumerate(lenses):
            cols[i].markdown(
                f"<span style='background-color:#eef2ff;"
                f"padding:6px 12px;border-radius:20px;'>"
                f"{lens.replace('_', ' ').title()}</span>",
                unsafe_allow_html=True
            )

    st.divider()

    # ---------- SUPPORTING EVIDENCE ----------
    st.subheader("📄 Supporting Evidence")

    if not evidence:
        st.warning("No strong evidence found for this query.")
    else:
        for e in evidence[:5]:
            st.markdown(
                f"<span class='transcript-badge'>Transcript ID: {e['transcript_id']}</span>",
                unsafe_allow_html=True
            )

            for t in e["factors"]:
                st.markdown(
                    f"<div class='evidence-box'>"
                    f"<span class='evidence-text'>• {t}</span>"
                 f"</div>",
                 unsafe_allow_html=True
                )

