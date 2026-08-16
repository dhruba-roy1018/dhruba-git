import json
from fastapi import APIRouter
from pydantic import BaseModel
from utils.llm import ask_gemini_text

router = APIRouter()

class MessageInput(BaseModel):
    message: str

PROMPT_TEMPLATE = """
You are a scam-detection assistant. Analyze this message (SMS/WhatsApp/email) for scam or legal red flags:

MESSAGE: "{message}"

Return ONLY valid JSON in this exact format, nothing else:
{{
  "red_flags": ["...", "..."],
  "risk_level": "Low/Medium/High",
  "safe_action": "ignore/verify/report",
  "explanation": "..."
}}
"""

@router.post("/check")
async def check_message(input: MessageInput):
    prompt = PROMPT_TEMPLATE.format(message=input.message)
    result_text = ask_gemini_text(prompt)
    try:
        cleaned = result_text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {"raw_response": result_text}