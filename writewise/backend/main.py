from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from fastapi import Body
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class RewriteRequest(BaseModel):
    text: str
    tone: str
    as_story: bool = False
    response_level: str = "elaborate"  # "brief", "elaborate", "comprehensive"

class RewriteResponse(BaseModel):
    rewritten_text: str
    title: str
    input_type: str

@app.post("/rewrite", response_model=RewriteResponse)
async def rewrite_text(request: RewriteRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    allowed_tones = [
        "Professional", "Friendly", "Casual", "Corporate", "Kids tone", "Gen Z tone", "Social media summary"
    ]
    if request.tone not in allowed_tones:
        raise HTTPException(status_code=400, detail=f"Invalid tone. Allowed: {', '.join(allowed_tones)}")

    # 1. Detect input type
    detect_prompt = f"Classify the following text as one of: email, story, article, resume, message, or other. Only return the type.\nText: {request.text}"
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
    rewrite_instructions = f"Rewrite the following text in a {request.tone} tone."
    if request.tone == "Social media summary":
        rewrite_instructions = "Summarize the following text for social media in a catchy, engaging way."
    if request.as_story or (input_type == "story"):
        rewrite_instructions += " Present it as a story."
    # Add response level instructions
    if request.response_level == "brief":
        rewrite_instructions += " Keep the response brief and concise."
    elif request.response_level == "elaborate":
        rewrite_instructions += " Provide an elaborate and detailed rewrite."
    elif request.response_level == "comprehensive":
        rewrite_instructions += " Make the rewrite comprehensive, covering all important aspects in depth."
    rewrite_prompt = f"{rewrite_instructions}\nText: {request.text}"

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
        raise HTTPException(status_code=500, detail=f"Rewrite failed: {str(e)}")

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

    return {"rewritten_text": rewritten, "title": title, "input_type": input_type}
class SocialRewriteRequest(BaseModel):
    text: str
    platform: str

class SocialRewriteResponse(BaseModel):
    platform_text: str
    posting_links: Dict[str, str]

@app.post("/social-rewrite", response_model=SocialRewriteResponse)
async def social_rewrite(request: SocialRewriteRequest = Body(...)):
    text = request.text
    platform = request.platform
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
    return {"platform_text": platform_text, "posting_links": links}

import urllib.parse

# --- Social Media Transformation Functions ---
def convert_to_instagram_tone(text: str) -> str:
    # Add hashtags, emojis, and make it engaging for Instagram
    hashtags = "#Inspiration #Motivation #Life #Story"
    return f"{text}\n\n{hashtags} \ud83d\udc4d\ud83d\ude0e"

def convert_to_facebook_tone(text: str) -> str:
    # Make it more personal and story-like for Facebook
    return f"{text}\n\nShare your thoughts below! \ud83d\udcdd"

def convert_to_linkedin_tone(text: str) -> str:
    # Make it professional and add a call to action for LinkedIn
    return f"{text}\n\nLet's connect and discuss! #ProfessionalGrowth"

def convert_to_twitter_tone(text: str) -> str:
    # Shorten and add hashtags for Twitter/X
    hashtags = "#AI #Rewrite #Productivity"
    return f"{text[:240]}... {hashtags}"

def convert_to_whatsapp_tone(text: str) -> str:
    # Make it conversational for WhatsApp
    return f"{text}\n\nSent via WriteWise \ud83d\udcbe"

def generate_social_media_links(platform: str, text: str) -> dict:
    encoded = urllib.parse.quote(text)
    links = {}
    if platform == "Instagram":
        # Instagram does not support prefilled posts via URL
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



@app.get("/")
async def root():
    return {"message": "Welcome to WriteWise API. Use the /rewrite endpoint to rewrite text."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
