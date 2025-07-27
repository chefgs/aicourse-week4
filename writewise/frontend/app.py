
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


# --- Social Media Platform Transformation Logic ---
import urllib.parse

def convert_to_instagram_tone(text):
    text = text.replace("!", " ✨").replace("great", "amazing").replace("good", "awesome")
    sentences = text.split('.')
    instagram_text = ""
    for sentence in sentences:
        if sentence.strip():
            instagram_text += sentence.strip() + " 💫\n"
    instagram_text += "\n👆 Double tap if you agree!\n#motivation #inspiration #success"
    return instagram_text

def convert_to_facebook_tone(text):
    text = text.replace("you", "we").replace("I think", "What do you think")
    facebook_text = "Hey friends! 👋\n\n" + text
    facebook_text += "\n\nWhat's your experience with this? Let me know in the comments! 💭"
    return facebook_text

def convert_to_linkedin_tone(text):
    text = text.replace("awesome", "valuable").replace("amazing", "significant").replace("!", ".")
    linkedin_text = "Professional insight: 💼\n\n" + text
    linkedin_text += "\n\nWhat are your thoughts on this approach? I'd love to hear from fellow professionals in the comments."
    linkedin_text += "\n\n#Leadership #BusinessStrategy #ProfessionalDevelopment"
    return linkedin_text

def convert_to_whatsapp_tone(text):
    text = text.replace("Hello", "Hey").replace(".", " 😊")
    whatsapp_text = "Hey! 👋\n\n" + text
    whatsapp_text += "\n\nLet me know what you think! 💭"
    return whatsapp_text

def convert_to_twitter_tone(text):
    words = text.split()
    if len(text) > 240:
        truncated = ' '.join(words[:30]) + "..."
        twitter_text = truncated + "\n\n🧵 Thread below 👇\n#TwitterThread"
    else:
        twitter_text = text + "\n\n#SocialMedia #ContentCreation"
    return twitter_text

def generate_social_media_links(platform, content):
    encoded_content = urllib.parse.quote(content)
    PRIYA_SOCIAL_LINKS = {
        'instagram': 'https://www.instagram.com/learn_ai_with_priya/',
        'facebook': 'https://www.facebook.com/profile.php?id=61578258155366',
        'linkedin': 'https://www.linkedin.com/in/priyawithai/',
        'whatsapp': 'https://wa.me/message/TXE74MCSDJTUO1'
    }
    links = {}
    if platform == 'Facebook':
        links['🚀 Post to Facebook'] = f"https://www.facebook.com/sharer/sharer.php?u=&quote={encoded_content}"
        links['📱 Visit Priya\'s Facebook'] = PRIYA_SOCIAL_LINKS['facebook']
    elif platform == 'Instagram':
        links['📱 Open Instagram App'] = "https://www.instagram.com/"
        links['🎯 Visit @learn_ai_with_priya'] = PRIYA_SOCIAL_LINKS['instagram']
        links['📸 Instagram Stories Camera'] = "https://www.instagram.com/stories/camera/"
        links['💼 Creator Studio (Desktop)'] = "https://business.facebook.com/creatorstudio/?tab=instagram_content_posts"
    elif platform == 'LinkedIn':
        links['💼 Post to LinkedIn'] = f"https://www.linkedin.com/feed/?shareActive=true&text={encoded_content}"
        links['🔗 Visit Priya\'s LinkedIn'] = PRIYA_SOCIAL_LINKS['linkedin']
    elif platform == 'Twitter/X':
        short_content = content[:250] + "..." if len(content) > 250 else content
        encoded_short = urllib.parse.quote(short_content)
        links['🐦 Tweet Now'] = f"https://twitter.com/intent/tweet?text={encoded_short}"
    elif platform == 'WhatsApp':
        links['💬 Send via WhatsApp'] = f"https://wa.me/?text={encoded_content}"
        links['📱 Message Priya'] = PRIYA_SOCIAL_LINKS['whatsapp']
    return links

# --- UI for Social Media Platform Selection and Posting ---
platform_options = ["None", "Instagram", "Facebook", "LinkedIn", "Twitter/X", "WhatsApp"]
platform_choice = st.selectbox("(Optional) Adapt for Social Media Platform:", platform_options)

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
                # Social media transformation
                platform_text = rewritten
                if platform_choice == "Instagram":
                    platform_text = convert_to_instagram_tone(rewritten)
                elif platform_choice == "Facebook":
                    platform_text = convert_to_facebook_tone(rewritten)
                elif platform_choice == "LinkedIn":
                    platform_text = convert_to_linkedin_tone(rewritten)
                elif platform_choice == "Twitter/X":
                    platform_text = convert_to_twitter_tone(rewritten)
                elif platform_choice == "WhatsApp":
                    platform_text = convert_to_whatsapp_tone(rewritten)
                # Show platform-optimized text
                if platform_choice != "None":
                    st.markdown(f"**{platform_choice} Optimized Text:**")
                    st.markdown(
                        f"<div style='background:#f0f2f6;padding:1em;border-radius:8px;color:#000'>{platform_text}</div>",
                        unsafe_allow_html=True
                    )
                    st.code(platform_text)
                    # Show posting links
                    links = generate_social_media_links(platform_choice, platform_text)
                    if links:
                        st.markdown("### 🔗 Direct Posting Links:")
                        for label, url in links.items():
                            st.markdown(f"- [{label}]({url})")
                else:
                    st.markdown(
                        f"<div style='background:#f0f2f6;padding:1em;border-radius:8px;color:#000'>{rewritten}</div>",
                        unsafe_allow_html=True
                    )
                    st.code(rewritten)
            except Exception as e:
                st.error(f"Error: {e}")
