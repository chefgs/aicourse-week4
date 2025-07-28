import os
import urllib.parse
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# --- Social Media Transformation Functions ---
def convert_to_instagram_tone(text: str) -> str:
    hashtags = "#Inspiration #Motivation #Life #Story"
    return f"{text}\n\n{hashtags} 👍😎"

def convert_to_facebook_tone(text: str) -> str:
    return f"{text}\n\nShare your thoughts below! 📝"

def convert_to_linkedin_tone(text: str) -> str:
    return f"{text}\n\nLet's connect and discuss! #ProfessionalGrowth"

def convert_to_twitter_tone(text: str) -> str:
    hashtags = "#AI #Rewrite #Productivity"
    return f"{text[:240]}... {hashtags}"

def convert_to_whatsapp_tone(text: str) -> str:
    return f"{text}\n\nSent via WriteWise 💾"

def generate_social_media_links(platform: str, text: str) -> dict:
    encoded = urllib.parse.quote(text)
    links = {}
    if platform == "Instagram":
        links["Instagram"] = "https://www.instagram.com/"
    elif platform == "Facebook":
        links["Facebook"] = f"https://www.facebook.com/sharer/sharer.php?u=&quote={encoded}"
    elif platform == "LinkedIn":
        links["LinkedIn"] = f"https://www.linkedin.com/sharing/share-offsite/?url=&summary={encoded}"
    elif platform == "Twitter/X":
        links["Twitter/X"] = f"https://twitter.com/intent/tweet?text={encoded}"
    elif platform == "WhatsApp":
        links["WhatsApp"] = f"https://api.whatsapp.com/send?text={encoded}"
    else:
        links[platform] = "#"
    return links

@app.route("/")
def root():
    return jsonify({"message": "Welcome to WriteWise Flask API. Use the /rewrite endpoint to rewrite text."})

@app.route("/rewrite", methods=["POST"])
def rewrite_text():
    data = request.json
    text = data.get("text", "")
    tone = data.get("tone", "")
    as_story = data.get("as_story", False)
    response_level = data.get("response_level", "elaborate")

    allowed_tones = [
        "Professional", "Friendly", "Casual", "Corporate", "Kids tone", "Gen Z tone", "Social media summary"
    ]
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
    if tone not in allowed_tones:
        return jsonify({"error": f"Invalid tone. Allowed: {', '.join(allowed_tones)}"}), 400

    # 1. Detect input type
    detect_prompt = f"Classify the following text as one of: email, story, article, resume, message, or other. Only return the type.\nText: {text}"
    try:
        detect_resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": detect_prompt}],
            max_tokens=10,
            temperature=0.0,
        )
        input_type = detect_resp.choices[0].message['content'].strip().lower()
    except Exception:
        input_type = "unknown"

    # 2. Build rewrite prompt with response level
    rewrite_instructions = f"Rewrite the following text in a {tone} tone."
    if tone == "Social media summary":
        rewrite_instructions = "Summarize the following text for social media in a catchy, engaging way."
    if as_story or (input_type == "story"):
        rewrite_instructions += " Present it as a story."
    if response_level == "brief":
        rewrite_instructions += " Keep the response brief and concise."
    elif response_level == "elaborate":
        rewrite_instructions += " Provide an elaborate and detailed rewrite."
    elif response_level == "comprehensive":
        rewrite_instructions += " Make the rewrite comprehensive, covering all important aspects in depth."
    rewrite_prompt = f"{rewrite_instructions}\nText: {text}"

    # 3. Rewrite text
    try:
        rewrite_resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional writer who rewrites text in different tones and formats."},
                {"role": "user", "content": rewrite_prompt}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        rewritten = rewrite_resp.choices[0].message['content'].strip()
    except Exception as e:
        return jsonify({"error": f"Rewrite failed: {str(e)}"}), 500

    # 4. Generate title
    try:
        title_prompt = f"Write a short, relevant title for the following text:\n{rewritten}"
        title_resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": title_prompt}],
            max_tokens=16,
            temperature=0.5,
        )
        title = title_resp.choices[0].message['content'].strip()
    except Exception:
        title = "Untitled"

    return jsonify({
        "rewritten_text": rewritten,
        "title": title,
        "input_type": input_type
    })

@app.route("/social-rewrite", methods=["POST"])
def social_rewrite():
    data = request.json
    text = data.get("text", "")
    platform = data.get("platform", "")
    if not text or not platform:
        return jsonify({"error": "Both text and platform are required."}), 400

    if platform == "Instagram":
        platform_text = convert_to_instagram_tone(text)
    elif platform == "Facebook":
        platform_text = convert_to_facebook_tone(text)
    elif platform == "LinkedIn":
        platform_text = convert_to_linkedin_tone(text)
    elif platform == "Twitter/X":
        platform_text = convert_to_twitter_tone(text)
    elif platform == "WhatsApp":
        platform_text = convert_to_whatsapp_tone(text)
    else:
        platform_text = text
    links = generate_social_media_links(platform, platform_text)
    return jsonify({
        "platform_text": platform_text,
        "posting_links": links
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)