from agent import run_agent

# initial example to directly call run_agent
msg = "Met Dr. Sneha Joshi at Fortis Hospital. Explained the advantages of our cardiac drug CardioPlus including reduced side effects and better patient recovery. Doctor appreciated the data and agreed to start prescribing it for selected patients. Follow up in two weeks to collect feedback."
print("run_agent output:", run_agent(msg))

# simulate chat merging logic manually using same helpers as main
import re as _re

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

def _is_correction_msg(msg: str) -> bool:
    return bool(_re.search(r"doctor(?:'s)? name (?:was|is) wrong|this is not|not .* but", msg, _re.IGNORECASE))

print("\nStateful chat tests:")
state = {}
def merge(new_data, prev_state, msg):
    merged = prev_state.copy()
    is_corr = _is_correction_msg(msg)
    for key, val in new_data.items():
        if not (val and val != "Unknown"):
            continue
        if is_corr and key in ("discussion", "outcome", "sentiment", "hospital", "material_shared"):
            continue
        if _mentions_field(msg, key) or is_corr:
            merged[key] = val
    merged["date"] = new_data.get("date")
    merged["time"] = new_data.get("time")
    return merged

msg1 = "Met Dr. Sharm at Fortis Hospital. He was positive."
data1 = run_agent(msg1)
print("new_data1:", data1)
state = merge(data1, state, msg1)
print("after msg1:", state)
msg2 = "Doctor name was wrong, this is Dr. Sharma."
data2 = run_agent(msg2)
print("new_data2:", data2)
state = merge(data2, state, msg2)
print("after msg2:", state)
msg3 = "Follow up in a month."
data3 = run_agent(msg3)
print("new_data3:", data3)
state = merge(data3, state, msg3)
print("after msg3:", state)
