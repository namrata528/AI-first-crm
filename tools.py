from langchain.tools import tool


@tool
def log_interaction_tool(notes: str):
    """Log interaction with doctor"""
    return f"Interaction logged: {notes}"


@tool
def edit_interaction_tool(notes: str):
    """Edit interaction notes"""
    return f"Interaction updated: {notes}"


@tool
def summarize_interaction_tool(notes: str):
    """Generate summary of doctor meeting"""
    return f"Summary: {notes[:100]}"


@tool
def followup_suggestion_tool(notes: str):
    """Suggest next follow-up"""
    return "Follow up with product brochure and next meeting."


@tool
def doctor_history_tool(name: str):
    """Fetch doctor interaction history"""
    return f"Fetching history for {name}"