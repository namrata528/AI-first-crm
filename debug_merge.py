from agent import run_agent
import re

_last = {}
def merge(new_data, prev, msg):
    merged = prev.copy()
    is_corr = bool(re.search(r"doctor(?:'s)? name (?:was|is) wrong|this is not|not .* but", msg, re.IGNORECASE))
    for k, v in new_data.items():
        if v and v != 'Unknown':
            merged[k] = v
    merged['date'] = new_data.get('date')
    merged['time'] = new_data.get('time')
    return merged

msgs = [
    "Met Dr. Sharm at Fortis Hospital. He was positive.",
    "Doctor name was wrong, this is Dr. Sharma.",
    "Follow up in a month."
]

for msg in msgs:
    print('msg:', msg)
    new = run_agent(msg)
    print('new_data', new)
    _last = merge(new, _last, msg)
    print('merged', _last)
    print('-' * 40)
