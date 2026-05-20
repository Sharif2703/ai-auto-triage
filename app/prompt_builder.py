import json

def build_prompt(failure_data):

    prompt = f"""
You are an AI QA triage assistant.

Analyze this failed test case.

Failure Details:
{json.dumps(failure_data, indent=2)}

Return:
- category
- root cause
- owner
- confidence
"""

    return prompt