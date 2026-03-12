from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from database import save_interaction

app = FastAPI()

# Allow React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat request model
class ChatRequest(BaseModel):
    message: str
    # previous state from earlier interactions, used for merging
    previous: dict | None = None


# Interaction save model
class InteractionRequest(BaseModel):
    doctor_name: str
    interaction_type: str | None = None
    date: str | None = None
    time: str | None = None
    attendees: str | None = None
    discussion: str | None = None
    sentiment: str | None = None
    outcome: str | None = None
    follow_up: str | None = None


# simple in-memory state to preserve fields across successive chat calls
_last_conversation: dict = {}

# helper to detect whether user's message is a simple correction
import re as _re

def _is_correction_msg(msg: str) -> bool:
    return bool(_re.search(r"doctor(?:'s)? name (?:was|is) wrong|this is not|not .* but", msg, _re.IGNORECASE))

# helper to check if message mentions a particular field
_field_patterns = {
    "doctor_name": r"\bdoctor\b|\bDr\b",
    "hospital": r"\bhospital\b",
    "discussion": r"\bdiscuss(?:ed|ion)?\b|\btalk(?:ed)? about\b",
    "outcome": r"\boutcome\b|\b(interested|not interested|agreed|will try|no interest)\b",
    "follow_up": r"\bfollow[-\s]?up\b",
    "sentiment": r"\bsentiment\b|\b(positive|negative|neutral)\b",
    "material_shared": r"\bbrochure|sample|flyer|material\b"
}

def _mentions_field(msg: str, field: str) -> bool:
    pat = _field_patterns.get(field)
    if not pat:
        return False
    return bool(_re.search(pat, msg, _re.IGNORECASE))

# CHAT ENDPOINT
@app.post("/chat")
def chat(req: ChatRequest):

    new_data = run_agent(req.message)
    merged = _last_conversation.copy()
    is_corr = _is_correction_msg(req.message)

    # merge with previous values: only update if message actually references that field
    for key, val in new_data.items():
        if not (val and val != "Unknown"):
            continue
        if is_corr and key in ("discussion", "outcome", "sentiment", "hospital", "material_shared"):
            # for correction messages, skip non-name fields
            continue
        if _mentions_field(req.message, key) or is_corr:
            merged[key] = val
    # always update timestamp to current call
    merged["date"] = new_data.get("date")
    merged["time"] = new_data.get("time")

    _last_conversation.clear()
    _last_conversation.update(merged)

    return {
        "response": "Interaction details extracted successfully",
        "doctor_name": merged.get("doctor_name"),
        "hospital": merged.get("hospital"),
        "discussion": merged.get("discussion"),
        "outcome": merged.get("outcome"),
        "follow_up": merged.get("follow_up"),
        "sentiment": merged.get("sentiment"),
        "material_shared": merged.get("material_shared"),
        "date": merged.get("date"),
        "time": merged.get("time")
    }


# SAVE INTERACTION
@app.post("/log_interaction")
def log_interaction(data: InteractionRequest):

    save_interaction(
        data.doctor_name,
        "Apollo Hospital",
        data.discussion,
        data.outcome,
        data.follow_up
    )

    return {"message": "Interaction saved"}