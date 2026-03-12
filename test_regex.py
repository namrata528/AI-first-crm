from agent import run_agent

# messages to test full extraction logic, including automatic fields and material detection
messages = [
    "Talked with Dr. John Doe at City Hospital. Discussed new hypertension drug; he was interested and wants follow up next week. Sentiment positive. Shared brochure.",
    "Dr Smith from County Medical Center not interested, will try after seeing sample, follow up in 5 days, sentiment negative.",
    "Met with Dr. Emily at Riverside Clinic; talked about diabetes management, neutral outcome, follow-up later.",
    "No doctor name mentioned but hospital General Hospital and outcome maybe later.",
    # user-provided problematic example
    "Met Dr. Sneha Joshi at Fortis Hospital. Explained the advantages of our cardiac drug CardioPlus including reduced side effects and better patient recovery. Doctor appreciated the data and agreed to start prescribing it for selected patients. Follow up in two weeks to collect feedback. Shared brochure."
]

for msg in messages:
    print("Message:", msg)
    result = run_agent(msg)
    print("Extracted:", result)
    print('-' * 60)

