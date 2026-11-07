# JanMitra — AI-Powered Government Schemes Helpline & Citizen Portal

> **"Har Yojana, Har Naagrik" (हर योजना, हर नागरिक)**  
> A civic-tech public utility connecting rural Indian citizens with central government welfare schemes through a free voice helpline in Hindi and an accessible companion web portal.

---

## Overview

Over 60% of eligible citizens in rural India miss out on government welfare benefits due to low digital literacy, language barriers, and complex official websites. **JanMitra** bridges this access gap through a two-channel platform:

1. **Voice Helpline (Primary Channel)**: A toll-free helpline where citizens speak naturally in Hindi, describe their needs, and receive spoken scheme recommendations followed by an SMS summary with official application links.
2. **Citizen Web Portal (Companion Channel)**: A fast, lightweight, bilingual (English/Hindi) portal designed for citizens and Common Service Centre (CSC) village operators to search, filter, and verify scheme eligibility.

---

## Key Features

- **Voice AI Pipeline**: End-to-end Hindi audio transcription (ASR), entity extraction, grounded scheme matching, and Hindi text-to-speech (TTS) audio generation.
- **Deterministic Eligibility Engine**: Evaluates applicant criteria (age, household annual income, gender, and category) against verified government scheme rules without AI hallucination.
- **Bilingual Interface**: Seamless instant toggle between English and Hindi (`data-en` / `data-hi`) across the entire web portal without page reloads.
- **Lightweight & Fast**: Pure semantic HTML5, custom CSS design tokens, and vanilla JavaScript (no heavy frontend frameworks or build steps), optimized for slow rural network connections.
- **Verified Scheme Database**: Indexed SQLite database with 22+ active central government welfare schemes across 10 categories (Agriculture, Health, Housing, Pension, Women & Child, Business & Loans, etc.).

---

## System Architecture

```
                    CITIZEN CHANNELS
              ┌───────────────────────────┐
              │  Voice Call (Toll-Free)   │
              │  Web Portal / CSC Kiosk   │
              └─────────────┬─────────────┘
                            │
               HTTP / REST  │  Twilio Webhooks
                            ▼
           ┌─────────────────────────────────┐
           │      FastAPI Backend Engine      │
           │                                 │
           │  ├── db.py (SQLite Queries)     │
           │  ├── matching.py (Eligibility)  │
           │  └── ai_pipeline.py (ASR/LLM/TTS)│
           └────────┬───────────────┬────────┘
                    │               │
     SQL Queries    │               │  Grounded Prompts
                    ▼               ▼
     ┌──────────────────────┐  ┌───────────────────────┐
     │   SQLite Database    │  │   Google Gemini API   │
     │   (Indexed Schemes)  │  │   (temp=0.0 Grounding)│
     └──────────────────────┘  └───────────────────────┘
```

---

## Project Structure

```
JanMitra/
├── backend/
│   ├── main.py              # FastAPI app & route definitions (/api/*)
│   ├── db.py                # Database connection, search, and pagination
│   ├── matching.py          # Deterministic eligibility matching engine
│   ├── ai_pipeline.py       # Speech transcription, Gemini RAG, and TTS synthesis
│   ├── test_pipeline.py     # Local CLI runner for the AI speech pipeline
│   ├── setup_database.py    # Database initialization & index creation
│   ├── sample_hindi.wav     # Sample Hindi voice recording for testing
│   └── requirements.txt     # Python backend dependencies
│
├── frontend/
│   ├── index.html           # Public citizen web portal
│   ├── css/
│   │   ├── base.css         # Custom properties, typography & reset
│   │   ├── layout.css       # Header, navigation, footer & grid
│   │   └── components.css   # Cards, wizard steps, badges & modal
│   └── js/
│       ├── lang.js          # Bilingual (EN/HI) translation system
│       ├── schemes.js       # Live search, category filters & details modal
│       └── checker.js       # 4-step eligibility self-assessment wizard
│
├── data/
│   ├── janmitra_schemes.db  # SQLite database with 22 verified schemes
│   ├── janmitra_schemes.csv # CSV export
│   └── janmitra_schemes_supervisor.xlsx # Excel data review
│
├── .gitignore               # Ignores .env, caches, logs, and generated audio
└── README.md                # This file
```

---

## REST API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/schemes` | List schemes with pagination (`page`, `limit`), `category` filter, and full-text `search`. |
| `GET` | `/api/schemes/{id}` | Full details for a single scheme row by ID (returns 404 if not found). |
| `GET` | `/api/categories` | Distinct categories with active scheme counts. |
| `POST` | `/api/match` | Deterministic matching against citizen profile (`age`, `income_annual`, `gender`, `category`). |

---

## Quickstart & Local Setup

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Install Dependencies
```bash
cd JanMitra/backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` in the project root or backend folder:
```bash
cp .env.example .env
```
Add your free Gemini API key from [Google AI Studio](https://aistudio.google.com/):
```env
GEMINI_API_KEY="your_api_key_here"
GEMINI_MODEL="gemini-2.5-flash"
```

### 4. Run the Backend Server
```bash
cd JanMitra/backend
uvicorn main:app --reload
```
- API root: `http://localhost:8000`
- Interactive Swagger docs: `http://localhost:8000/docs`

### 5. Test the AI Speech Pipeline Locally
```bash
cd JanMitra/backend
python test_pipeline.py --audio sample_hindi.wav
```
This transcribes the Hindi audio, extracts the citizen profile via Gemini, matches schemes, and synthesizes `output_response.mp3`.

### 6. Run the Citizen Web Portal
Open `JanMitra/frontend/index.html` in your web browser (or serve it with VS Code Live Server / `python -m http.server 5500`).

---

## License

This project is licensed under the MIT License for public civic-tech and social welfare development.
