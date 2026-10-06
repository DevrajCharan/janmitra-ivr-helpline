# JanMitra Call: Comprehensive Project Workflow & Role Distribution

## 1. Revised Team Roles & Responsibilities
Based on the team's strengths and preferences (Yash on Database, Kajal on Frontend/APIs), here is the optimized distribution to ensure parallel development without bottlenecks:

| S.No. | Team Member | Primary Role | Core Responsibilities |
| :---: | :--- | :--- | :--- |
| 1 | **Yash Burad** | **Database Architecture & Data Curation** | Designing the schema for government schemes, setting up PostgreSQL/MongoDB and a Vector DB (Chroma/Pinecone) for AI search. Scraping and manually entering 20-30 pilot schemes. |
| 2 | **Kajal Pareek** | **Frontend Development & API Integration** | Building the web interface (Landing page + Admin dashboard to add schemes + Web-based scheme search). Connecting the frontend UI to backend REST APIs. |
| 3 | **Devraj Charan** | **Team Lead & Telephony Architecture** | Orchestrating Twilio. Handling the call flow logic (TwiML), routing calls to the backend, managing call states (greeting -> recording -> playback), and integrating SMS. |
| 4 | **Suryansh Raghuwanshi** | **Backend Engineering & Services** | Building the core backend server (Python/FastAPI or Node.js) that acts as the brain. It will receive Twilio webhooks, route data to the AI, and serve Kajal's frontend. |
| 5 | **Tarun Yadav** | **AI/NLP Pipeline & Speech Tech** | Handling Speech-to-Text (ASR) and Text-to-Speech (TTS). Writing the Gemini API prompts (Prompt Engineering) and implementing Retrieval-Augmented Generation (RAG) with Yash's database. |
| 6 | **Utsang Kumar Jain** | **Testing, Deployment & Community Field Study** | Deploying the app to the cloud (Render/Vercel/AWS). Conducting usability tests with actual users. Maintaining the EPICS logbook and formatting the final college report. |

---

## 2. Recommended Technology Stack
To prevent getting stuck with incompatible technologies, stick to this modern, well-documented stack:
* **Backend:** Python with **FastAPI** (Python is easiest for integrating AI/Gemini).
* **Frontend (Website):** **React.js** (or plain HTML/JS/TailwindCSS if keeping it simple).
* **Database:** **Supabase** (Free PostgreSQL) + **ChromaDB** (for AI vector search).
* **Telephony & SMS:** **Twilio** (Use the free student/developer tier for testing).
* **AI & LLM:** **Google Gemini API** (Free tier is generous and powerful).
* **Speech-to-Text (ASR) & TTS:** **Google Cloud Speech API** or **OpenAI Whisper** (fast and accurate for Indian accents).
* **Hosting/Deployment:** **Render** or **Railway** (for the FastAPI backend), **Vercel** (for the frontend).

---

## 3. Phase-by-Phase Execution Plan

### Phase 1: Foundation & Prototyping (Weeks 1-3)
* **Goal:** Set up the environment and get a basic "Hello World" working across all pieces.
* **Yash:** Define the database schema (Columns: Scheme Name, Age Limit, Income Limit, Category, Benefits, Process). Create an Excel sheet with 20 real schemes to start.
* **Kajal:** Create the wireframes/UI for the website. Build a static landing page explaining the JanMitra toll-free number.
* **Suryansh:** Set up the basic FastAPI server. Create a simple API endpoint (e.g., `GET /schemes`).
* **Devraj:** Buy a free Twilio test number. Set up a webhook so that when someone calls the number, Twilio hits Suryansh's FastAPI endpoint and says "Hello, welcome to JanMitra".
* **Tarun:** Get Gemini API keys. Write a simple Python script that takes a hardcoded text question and returns an answer from Gemini.

### Phase 2: Data & AI Integration (Weeks 4-6)
* **Goal:** Connect the Database to the AI so the AI can answer questions about the schemes (RAG Pipeline).
* **Yash:** Push the Excel data into the actual database (Supabase/PostgreSQL).
* **Tarun & Yash:** Work together to convert the scheme data into "embeddings" (vectors) so Gemini can search through them quickly based on user queries.
* **Suryansh & Kajal:** Suryansh builds the API to fetch schemes; Kajal connects the website to this API so users can search schemes visually on the website.

### Phase 3: The Voice Pipeline (Weeks 7-9)
* **Goal:** Make the system understand spoken words and reply with spoken words.
* **Devraj & Tarun:** Configure Twilio to record the user's voice and send the audio file to the backend.
* **Tarun & Suryansh:** The backend receives the audio, sends it to Speech-to-Text (Whisper/Google) -> converts to text -> sends text to Gemini -> gets the answer -> sends answer to Text-to-Speech (TTS) -> returns the audio link to Twilio.
* **Devraj:** Make Twilio play the generated audio back to the caller.

### Phase 4: Refinement & SMS (Weeks 10-11)
* **Goal:** Polish the experience and add the SMS follow-up.
* **Devraj & Suryansh:** After the call ends, trigger Twilio SMS to send a summary text (e.g., "You are eligible for PM-Kisan. Apply here: [link]").
* **Kajal:** Complete the "Admin Dashboard" on the website where Yash can easily add or edit new schemes without touching the code.
* **Utsang:** Test the full loop. Call the number, speak in different accents, try to break the system. Log all bugs.

### Phase 5: Deployment & Final Review (Weeks 12-14)
* **Goal:** Move from localhost to the internet, ready for the supervisor demo.
* **Utsang & Suryansh:** Deploy the backend on Render/Railway. Deploy the frontend on Vercel. Update Twilio webhooks to point to the live server URL.
* **Utsang:** Conduct a community test (have 5-10 people outside your team call the number). Record their feedback for the EPICS record book.
* **Whole Team:** Prepare the final presentation, architecture diagrams, and report based on the literature review.

---

## 4. Critical "Anti-Stuck" Strategies (Read Carefully)

1. **The Twilio Ngrok Trap:** During development, Twilio needs a public URL to communicate with your local backend. You *must* use a tool called **ngrok** to expose your localhost to the internet. If you don't do this, Twilio will fail silently.
2. **The Audio Latency Problem:** Processing Speech -> AI -> Speech takes time. Callers might hang up if there is dead silence. **Solution:** Program Twilio to say *"Please hold on while I find the best schemes for you..."* immediately after they finish speaking, buying your backend 3-5 seconds to process the AI response.
3. **Database Hallucinations:** Do not let Gemini rely on its own memory. You must strictly prompt it: *"You are JanMitra. Only answer based on the provided database context. If the scheme is not in the context, say you don't know."*
4. **Website Scope Creep:** Keep the website simple! The core project is the IVR call. The website should just be a clean landing page and an admin interface. Don't waste weeks making a complex user dashboard.
