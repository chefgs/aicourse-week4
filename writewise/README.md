# WriteWise – Smarter Document Rewriter

## Product Requirements Document (PRD)

### Overview
WriteWise is an AI-powered document rewriting tool that allows users to input any text and instantly rewrite it in a variety of tones and formats. The app leverages OpenAI's GPT models to:
- Rewrite text in a selected tone (Professional, Friendly, Casual, Corporate, Kids, Gen Z, Social Media Summary)
- Detect the nature of the input (e.g., email, story, article, resume)
- Optionally rewrite as a story
- Generate a relevant title for the rewritten content

### Target Users
- Professionals, students, marketers, parents, and anyone who needs to quickly adapt text for different audiences or platforms.

### Core Features
1. **Text Rewriting & Tone Adjustment**
    - Supported tones: Professional, Friendly, Casual, Corporate, Kids tone, Gen Z tone, Social media summary
2. **Input Type Detection**
    - Detects if the input is an email, story, article, resume, message, or other
3. **Rewrite as Story**
    - Option to force rewrite as a story, or auto-applies if input is a story
4. **Title Generation**
    - Generates a short, relevant title for the rewritten content
5. **User Interface**
    - Streamlit-based, with text input, tone selection, "Rewrite as story" toggle, and output display
6. **API**
    - FastAPI backend with `/rewrite` endpoint

### User Flow
1. User enters or pastes text
2. User selects a tone and optionally toggles "Rewrite as story"
3. User clicks "Rewrite Text"
4. App displays:
    - Detected input type
    - Generated title
    - Rewritten text (with copy option)

### Non-Goals
- Not a plagiarism checker or grammar corrector
- Not a long-form content generator

---

## Technical Documentation

### Backend (FastAPI)
- **Endpoint:** `POST /rewrite`
- **Request Body:**
    ```json
    {
      "text": "original input",
      "tone": "Professional" | "Friendly" | "Casual" | "Corporate" | "Kids tone" | "Gen Z tone" | "Social media summary",
      "as_story": true | false
    }
    ```
- **Response:**
    ```json
    {
      "rewritten_text": "...",
      "title": "...",
      "input_type": "email" | "story" | "article" | "resume" | "message" | "other" | "unknown"
    }
    ```
- **Logic:**
    1. Detect input type using GPT
    2. Rewrite text in selected tone (and as story if requested)
    3. Generate a title for the rewritten content


### Frontend (Streamlit)
- **Features:**
    - Text input area (multi-line)
    - Tone selection (radio buttons)
    - "Rewrite as story" checkbox
    - Response detail level (brief, elaborate, comprehensive)
    - Use Sample Text dropdown (multiple categories)
    - Social Media Platform selection (Instagram, Facebook, LinkedIn, Twitter/X, WhatsApp)
    - Platform-optimized text transformation and display
    - Direct posting links for each platform (where supported)
    - Submit button
    - Display detected input type, generated title, and rewritten text
    - Copy output button
    - Loading spinner during API call
    - Error/info messages as needed

### Example UI Layout
```
------------------------------------------------------
| WriteWise – Smarter Document Rewriter             |
| [Text input area]                                 |
| [Tone selection: radio buttons]                   |
| [ ] Rewrite as story (checkbox)                   |
| [Rewrite Text] [Use Sample Text]                  |
------------------------------------------------------
| Detected input type: [e.g., email]                |
| Title: [generated title]                          |
| [Rewritten text in styled box]                    |
| [Copy Output]                                     |
------------------------------------------------------
```

### Development Workflow (AI Code Tools)
1. **Define/Refine PRD and UI/UX in README**
2. **Generate backend and frontend code using AI tools**
3. **Iterate on features and bugfixes via AI code suggestions**
4. **Test locally using `run.sh` or manual commands**
5. **Deploy backend (Railway/Render) and frontend (Streamlit Cloud/locally)**

### Environment Variables
- `OPENAI_API_KEY` – required for backend
- `API_URL` – used by frontend to connect to backend

### Example .env
```
OPENAI_API_KEY=your_openai_api_key_here
API_URL=http://localhost:8000
```

---

## Future Enhancements (Optional)
- Add more tones or custom tone input
- Support for additional input types
- User authentication and history
- Export rewritten content (PDF, DOCX, etc.)

---

## License
[Include your license information here]
# WriteWise - Document Rewriter

WriteWise is an AI-powered document rewriting application that transforms text to different tones using OpenAI GPT.

## Features

- Rewrite text in Professional, Casual, or Friendly tones
- Simple and intuitive user interface
- Fast API backend for AI processing
- Copy output to clipboard functionality

## Project Structure

```
writewise/
├── backend/
│   ├── main.py        # FastAPI app with /rewrite route
│   └── requirements.txt
├── frontend/
│   ├── app.py         # Streamlit UI
│   └── requirements.txt
└── .env.example       # Template for environment variables
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd writewise
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key.

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at http://localhost:8000

> **Note:** If you encounter issues with `pydantic-core` installation, try these solutions:
> 1. Make sure you have the necessary build tools: `pip install wheel setuptools`
> 2. Use a virtual environment: `python -m venv venv && source venv/bin/activate`
> 3. Upgrade pip: `pip install --upgrade pip`

### 4. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The frontend will be available at http://localhost:8501

## Deployment

### Backend Deployment (Railway or Render)

1. Create an account on Railway or Render
2. Set up a new project and connect to your repository
3. Set the environment variable `OPENAI_API_KEY`
4. Deploy the backend from the `/backend` directory

### Frontend Deployment (Streamlit Cloud)

1. Create an account on Streamlit Cloud
2. Connect to your repository
3. Point to `/frontend/app.py` as the main file
4. Set the environment variable `API_URL` to your backend URL

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI**: OpenAI GPT-3.5/GPT-4
- **Deployment**: Railway/Render (backend), Streamlit Cloud (frontend)

## License

[Include your license information here]
