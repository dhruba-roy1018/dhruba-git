import os
import shutil
import json
from fastapi import APIRouter, UploadFile, File
from utils.llm import ask_gemini_with_file

router = APIRouter()

PROMPT = """
You are a legal risk assistant. The attached file is a contract or agreement (photo or PDF).
1. Extract the key clauses.
2. For each risky clause, give: the clause text, a risk score (Low/Medium/High),
   a plain-English "what could go wrong" explanation, and a suggested negotiation question.
Return ONLY valid JSON in this exact format, nothing else:
{
  "clauses": [
    {"text": "...", "risk": "High", "explanation": "...", "negotiation_question": "..."}
  ],
  "overall_risk": "Medium"
}
"""

@router.post("/scan")
async def scan_contract(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result_text = ""
    try:
        result_text = ask_gemini_with_file(temp_path, PROMPT)
        cleaned = result_text.strip().removeprefix("```json").removesuffix("```").strip()
        result_json = json.loads(cleaned)
    except Exception as e:
        result_json = {"error": str(e), "raw": result_text}
    finally:
        os.remove(temp_path)

    return result_json