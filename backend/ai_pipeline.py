import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
load_dotenv()
GEMINI_SYSTEM_PROMPT = """
You are JanMitra, a helpful government scheme assistant for rural Indian citizens.
RULES — FOLLOW STRICTLY:
1. You ONLY answer using the scheme information in CONTEXT below.
2. If the answer is not in CONTEXT, say exactly:
   "मुझे इस योजना की जानकारी नहीं है।
    कृपया सरकारी पोर्टल पर जाँचें या
    1800-XXX-XXXX पर कॉल करें।"
3. Never invent scheme names, benefit amounts, or eligibility criteria.
4. Keep your answer under 100 words. This is played over a phone call.
5. Use simple Hindi a villager understands. No bureaucratic language.
6. Always end by stating the official portal URL clearly.
CONTEXT (schemes the citizen qualifies for — from verified database only):
{matched_schemes_json}
CITIZEN'S TRANSCRIBED QUERY:
{transcribed_text}
"""
_NO_SCHEMES_MESSAGE = (
    "मुझे इस योजना की जानकारी नहीं है। कृपया सरकारी पोर्टल पर जाँचें या "
    "1800-XXX-XXXX पर कॉल करें।"
)
def _cloud_credentials_configured() -> bool:
    credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    return bool(credentials and Path(credentials).is_file())
def _transcribe_with_google(audio_path: str) -> str:
    from google.cloud import speech
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=Path(audio_path).read_bytes())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=os.getenv("ASR_LANGUAGE_CODE", "hi-IN"),
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join(
        result.alternatives[0].transcript
        for result in response.results
        if result.alternatives
    ).strip()
def _transcribe_with_speech_recognition(audio_path: str) -> str:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(
        audio, language=os.getenv("ASR_LANGUAGE_CODE", "hi-IN")
    ).strip()
def transcribe_audio(audio_path: str) -> str:
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Audio file not found / ऑडियो फ़ाइल नहीं मिली: {path}"
        )
    errors: list[str] = []
    if _cloud_credentials_configured():
        try:
            text = _transcribe_with_google(str(path))
            if text:
                return text
        except Exception as error:
            errors.append(f"Google Cloud ASR: {error}")
    try:
        text = _transcribe_with_speech_recognition(str(path))
        if text:
            return text
    except Exception as error:
        errors.append(f"SpeechRecognition fallback: {error}")
    detail = "; ".join(errors) or "No speech was detected / आवाज़ नहीं मिली"
    raise RuntimeError(
        f"Speech transcription failed / आवाज़ को शब्दों में बदलना विफल: {detail}"
    )
def _gemini_model() -> Any:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise RuntimeError(
            "GEMINI_API_KEY is missing / GEMINI_API_KEY उपलब्ध नहीं है।"
        )
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
def extract_intent(transcribed_text: str) -> dict[str, Any]:
    if not transcribed_text.strip():
        raise ValueError("Transcribed text is empty / ट्रांसक्राइब किया गया पाठ खाली है।")
    model = _gemini_model()
    prompt = (
        "Extract this citizen profile from Hindi speech. Return only JSON with exactly "
        'these keys: age (integer or null), income_annual (integer or null), '
        'category (string or null), gender ("Male", "Female", or "All"). '
        "Use null when speech does not provide a value. Do not infer missing values. "
        "Known categories: Agriculture, Health, Housing, Pension, Women & Child, "
        "Business & Loans, Financial Inclusion, Education, Disability, "
        "Skill & Employment.\n\nSpeech:\n" + transcribed_text
    )
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "response_mime_type": "application/json",
        },
    )
    try:
        profile = json.loads(response.text)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Gemini returned invalid profile JSON / Gemini ने गलत JSON दिया: {error}"
        ) from error
    if set(profile) != {"age", "income_annual", "category", "gender"}:
        raise ValueError("Gemini profile shape is invalid / प्रोफ़ाइल का प्रारूप गलत है।")
    age = profile["age"]
    income = profile["income_annual"]
    if age is not None and (
        not isinstance(age, int) or isinstance(age, bool) or not 1 <= age <= 120
    ):
        raise ValueError("Invalid age / उम्र अमान्य है।")
    if income is not None and (
        not isinstance(income, int) or isinstance(income, bool) or income < 0
    ):
        raise ValueError("Invalid income / आमदनी अमान्य है।")
    if profile["category"] is not None and not isinstance(profile["category"], str):
        raise ValueError("Invalid category / श्रेणी अमान्य है।")
    if profile["gender"] not in {"Male", "Female", "All"}:
        raise ValueError("Invalid gender / लिंग अमान्य है।")
    return profile
def generate_grounded_response(query_text: str, matched_schemes: list) -> str:
    if not matched_schemes:
        return _NO_SCHEMES_MESSAGE
    context = json.dumps(matched_schemes, ensure_ascii=False, sort_keys=True)
    prompt = GEMINI_SYSTEM_PROMPT.format(
        matched_schemes_json=context, transcribed_text=query_text
    )
    response = _gemini_model().generate_content(
        prompt, generation_config={"temperature": 0.0}
    )
    answer = response.text.strip()
    if not answer:
        raise RuntimeError("Gemini returned an empty answer / Gemini ने खाली उत्तर दिया।")
    if len(answer.split()) > 100:
        raise RuntimeError("Gemini response exceeded 100 words / उत्तर 100 शब्दों से लंबा है।")
    return answer
def _synthesize_with_google(hindi_text: str, output_path: str) -> None:
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()
    audio = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=hindi_text),
        voice=texttospeech.VoiceSelectionParams(
            language_code=os.getenv("TTS_LANGUAGE_CODE", "hi-IN"),
            name=os.getenv("TTS_VOICE_NAME", "hi-IN-Standard-A"),
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        ),
    )
    Path(output_path).write_bytes(audio.audio_content)
def synthesize_speech(hindi_text: str, output_path: str) -> str:
    if not hindi_text.strip():
        raise ValueError("Hindi text is empty / हिंदी पाठ खाली है।")
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    if _cloud_credentials_configured():
        try:
            _synthesize_with_google(hindi_text, str(destination))
            return str(destination)
        except Exception as error:
            errors.append(f"Google Cloud TTS: {error}")
    try:
        from gtts import gTTS
        gTTS(text=hindi_text, lang="hi", slow=False).save(str(destination))
        return str(destination)
    except Exception as error:
        errors.append(f"gTTS fallback: {error}")
    raise RuntimeError(
        "Speech synthesis failed / आवाज़ बनाना विफल हुआ: " + "; ".join(errors)
    )
