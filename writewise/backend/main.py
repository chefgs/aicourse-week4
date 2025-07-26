
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

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

@app.get("/")
async def root():
    return {"message": "Welcome to WriteWise API. Use the /rewrite endpoint to rewrite text."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
