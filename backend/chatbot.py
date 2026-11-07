import os
import re
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from db import search_schemes

load_dotenv()

router = APIRouter()

CHATBOT_SYSTEM_PROMPT = """
You are JanMitra Assistant, a helpful bilingual guide for the JanMitra government scheme portal.

RULES — FOLLOW STRICTLY:
1. Answer ONLY using the scheme context provided in <context> tags and your knowledge of
   the JanMitra website (scheme categories, eligibility wizard, helpline).
2. If the answer is not in the context, say:
   - English: "I don't have that information. Please call the helpline: 1800-XXX-XXXX"
   - Hindi: "मुझे यह जानकारी नहीं है। कृपया हेल्पलाइन पर कॉल करें: 1800-XXX-XXXX"
3. Never invent scheme names, benefit amounts, or eligibility rules.
4. Keep answers under 80 words. Citizens read this on a phone screen.
5. Match the language the citizen used — reply in Hindi if they wrote Hindi.
6. Never discuss politics, religion, or anything unrelated to government schemes.
7. If asked about the site: explain the category grid, eligibility wizard, scheme cards,
   and that the helpline is free and answered in Hindi.
8. For unrelated requests such as jokes, politely refuse in the citizen's language and
   remind them that you only help with government schemes.

<context>
{scheme_context}
</context>
"""

CHAT_UNAVAILABLE = (
    "Chat service unavailable. Please call the helpline: 1800-XXX-XXXX / "
    "चैट सेवा उपलब्ध नहीं। हेल्पलाइन पर कॉल करें।"
)


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=500)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    history: list[ChatMessage] = Field(default_factory=list)


def detect_language(message: str) -> str:
    devanagari = len(re.findall(r"[\u0900-\u097f]", message))
    letters = len(re.findall(r"[^\W\d_]", message, flags=re.UNICODE))
    return "hi" if letters and devanagari / letters > 0.3 else "en"


def _keywords(message: str) -> list[str]:
    words = re.findall(r"[\w\u0900-\u097f]+", message.casefold())
    return [word for word in words if len(word) > 1]


def retrieve_schemes(message: str) -> list[dict[str, Any]]:
    schemes: dict[int, dict[str, Any]] = {}
    for keyword in _keywords(message):
        result = search_schemes(keyword, None, 1, 5)
        for scheme in result["schemes"]:
            schemes[scheme["id"]] = scheme
        if len(schemes) >= 5:
            break
    return list(schemes.values())[:5]


def _ollama_payload(request: ChatRequest, schemes: list[dict[str, Any]]) -> dict[str, Any]:
    context = "\n\n".join(
        f"Scheme: {scheme['scheme_name']}\n"
        f"Hindi name: {scheme['hindi_name']}\n"
        f"Category: {scheme['category']}\n"
        f"Benefits: {scheme['benefits']}\n"
        f"Amount: {scheme['benefit_amount']}\n"
        f"Eligibility: {scheme['beneficiary_type']}\n"
        f"Official portal: {scheme['portal_url']}"
        for scheme in schemes
    ) or "No matching schemes were found in the verified database."
    messages = [
        {"role": "system", "content": CHATBOT_SYSTEM_PROMPT.format(scheme_context=context)}
    ]
    messages.extend({"role": item.role, "content": item.content} for item in request.history[-5:])
    messages.append({"role": "user", "content": request.message})
    return {
        "model": os.getenv("OLLAMA_MODEL", "gemma2:2b"),
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1},
    }


@router.post("/api/chat")
def chat(request: ChatRequest) -> dict[str, Any]:
    language = detect_language(request.message)
    schemes = retrieve_schemes(request.message)
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    try:
        response = httpx.post(
            f"{base_url}/api/chat",
            json=_ollama_payload(request, schemes),
            timeout=15.0,
        )
        response.raise_for_status()
        payload = response.json()
        reply = payload.get("message", {}).get("content", "").strip()
        if not reply:
            raise RuntimeError("Ollama returned an empty reply")
    except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError, ValueError, RuntimeError) as error:
        raise HTTPException(status_code=503, detail=CHAT_UNAVAILABLE) from error
    return {
        "reply": reply,
        "lang": language,
        "context_schemes": [scheme["scheme_name"] for scheme in schemes],
    }
