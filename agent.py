import requests
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def run_agent(message):
    """
    Extract structured HCP interaction data from free text.
    Returns a dict with keys:
    doctor_name, hospital, discussion, outcome, followup, sentiment
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an AI assistant for pharma sales CRM.

Extract the following fields and return ONLY JSON:

doctor_name
hospital
discussion
outcome
follow_up
sentiment

Text:
{message}
"""
    # note: prompt is returned in output so frontend can display what was sent to model

    # (prompt is not logged to avoid exposing to downstream systems)

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        data = response.json()
    except Exception as e:
        print("Groq API error:", e)
        data = {}

    # Extract JSON from LLM response
    result = {}
    try:
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        json_text = re.search(r"\{.*\}", text, re.DOTALL)
        if json_text:
            result = json.loads(json_text.group())
    except Exception as e:
        print("JSON parse error:", e)
        result = {}

    # -------- Regex fallback extraction --------
    def regex_fallback(pattern, default="Unknown", flags=0):
        match = re.search(pattern, message, flags)
        return match.group().strip() if match else default

    # Doctor name (Dr. Lastname Firstname)
    if not result.get("doctor_name"):
        result["doctor_name"] = regex_fallback(
            r"\bDr\.?\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b"
        )

    # Hospital / clinic
    if not result.get("hospital"):
        result["hospital"] = regex_fallback(
            r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*(?:\s+(?:Hospital|Medical Center|Clinic|Institute))\b"
        )

    # Discussion - try to extract just the topic using common verbs
    if not result.get("discussion"):
        topic_match = re.search(
            r"\b(?:discussed|talked about|about|explained|presented|demonstrated|shown)\s+([^\.\n]+)",
            message,
            re.IGNORECASE
        )
        if topic_match:
            result["discussion"] = topic_match.group(1).strip()
        else:
            # fallback to first sentence if no keyword found
            result["discussion"] = message.split(".")[0].strip()

    # if discussion still seems too generic (e.g. entire message) try a more aggressive cleanup
    if result.get("discussion") and (result["discussion"] == message or len(result["discussion"]) < 10):
        # strip doctor/hospital prefix
        cleaned = re.sub(
            r"Met\s+Dr\.?\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+at\s+[A-Z][A-Za-z\s]+?[\.]?",
            "",
            message,
            flags=re.IGNORECASE,
        )
        # capture text until a stopping keyword like outcome or follow-up
        stop_match = re.search(r"(.+?)(?:\.|\b(interested|not interested|positive|negative|follow[-\s]?up)\b)", cleaned, re.IGNORECASE)
        if stop_match:
            result["discussion"] = stop_match.group(1).strip()
        else:
            result["discussion"] = cleaned.split(".")[0].strip()

    # Outcome (common pharma phrases)
    if not result.get("outcome"):
        # extend with 'agreed to' and similar
        result["outcome"] = regex_fallback(
            r"\b(interested|not interested|no interest|will try|will not try|maybe later|needs more info|agreed to (?:start )?prescrib(?:e|ing)?|agreed to use|appreciated)\b",
            default="Unknown",
            flags=re.IGNORECASE
        )

    # Follow-up (capture any words after 'follow up' until period or newline)
    if not result.get("follow_up"):
        follow_match = re.search(r"follow[-\s]?up\b[^\.\n]*", message, re.IGNORECASE)
        if follow_match:
            result["follow_up"] = follow_match.group().strip()
        else:
            result["follow_up"] = "Unknown"

    # Sentiment – look for explicit words first, otherwise simple heuristics
    if not result.get("sentiment"):
        sentiment_match = re.search(r"\b(positive|negative|neutral)\b", message, re.IGNORECASE)
        if sentiment_match:
            result["sentiment"] = sentiment_match.group().capitalize()
        else:
            # check for positive/negative keywords
            if re.search(r"\b(appreciated|agreed|pleased|happy|good|great|positive)\b", message, re.IGNORECASE):
                result["sentiment"] = "Positive"
            elif re.search(r"\b(disappointed|not interested|concerned|negative|bad)\b", message, re.IGNORECASE):
                result["sentiment"] = "Negative"
            else:
                result["sentiment"] = "Neutral"

    # material shared detection (brochure, sample etc.)
    material_match = re.search(r"\b(brochure|brocher|sample|flyer|presentation|material)\b", message, re.IGNORECASE)
    material_shared = material_match.group().lower() if material_match else "None"

    # add timestamp fields (date and time)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # allow user corrections such as "this is not Sharma this is Varma"
    corr = re.search(
        r"(?:this is not|not)\s+([A-Z][a-zA-Z]+)\s*(?:,?\s*(?:this is|but)\s+([A-Z][a-zA-Z]+))",
        message,
        re.IGNORECASE,
    )
    if corr:
        correct = corr.group(2) or corr.group(1)
        result["doctor_name"] = correct.strip()

    # prepare filled dictionary (prompt is not included for logform)
    filled = {
        "doctor_name": result.get("doctor_name", "Unknown"),
        "hospital": result.get("hospital", "Unknown"),
        "discussion": result.get("discussion", "Unknown"),
        "outcome": result.get("outcome", "Unknown"),
        "follow_up": result.get("follow_up", "Unknown"),
        "sentiment": result.get("sentiment", "Neutral"),
        "material_shared": material_shared,
        "date": date_str,
        "time": time_str
    }

    return filled
