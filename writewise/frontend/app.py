
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="WriteWise – Smarter Document Rewriter", page_icon="📝", layout="centered")

st.title("WriteWise – Smarter Document Rewriter")
st.write("Transform your text with AI-powered tone adjustments.")


# Sample text options
sample_texts = {
    "Payment Request": "We'd like to inform you that your payment is past due. Please make a payment as soon as possible to avoid additional fees. If you have any questions, contact our support team.",
    "Story": "Once upon a time, a little girl found a mysterious key in her backyard. She wondered what it could unlock.",
    "Job Happy News": "Congratulations! We are pleased to offer you the position. Welcome to the team!",
    "Sad News": "We regret to inform you that your application was not successful this time.",
    "Business News": "Our company has achieved record growth this quarter, thanks to the dedication of our employees and support from our clients."
}

sample_choice = st.selectbox("Choose a sample text to load:", ["None"] + list(sample_texts.keys()))
if sample_choice != "None":
    st.session_state['input_text'] = sample_texts[sample_choice]

text = st.text_area("Enter your text below:", value=st.session_state.get('input_text', ''), height=200, key="input_text")
tone_options = [
    "Professional",
    "Friendly",
    "Casual",
    "Corporate",
    "Kids tone",
    "Gen Z tone",
    "Social media summary"
]
tone = st.radio("Select the tone for rewriting:", tone_options, horizontal=True)

as_story = st.checkbox("Rewrite as a story (if possible)")

# Response level selection
level_options = {
    "Brief summary": "brief",
    "Elaborate": "elaborate",
    "Comprehensive": "comprehensive"
}
level_label = st.radio("Select response detail level:", list(level_options.keys()), horizontal=True)
response_level = level_options[level_label]

if st.button("Rewrite Text"):
    if not text.strip():
        st.info("Please enter some text to rewrite.")
    else:
        with st.spinner("Rewriting your text..."):
            try:
                payload = {
                    "text": text,
                    "tone": tone,
                    "as_story": as_story,
                    "response_level": response_level
                }
                resp = requests.post(f"{API_URL}/rewrite", json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                title = data.get("title", "")
                rewritten = data.get("rewritten_text", "")
                input_type = data.get("input_type", "")
                if input_type:
                    st.info(f"Detected input type: {input_type}")
                if title:
                    st.markdown(f"#### {title}")
                st.markdown(
                    f"<div style='background:#f0f2f6;padding:1em;border-radius:8px;color:#000'>{rewritten}</div>",
                    unsafe_allow_html=True
                )
                st.code(rewritten)
            except Exception as e:
                st.error(f"Error: {e}")
