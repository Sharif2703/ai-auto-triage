import json
import os

from ai_engine import ask_ai
from prompt_builder import build_prompt
from report_writer import save_report

FAILURES_DIR = "../failures"

summary = {
    "total_failures": 0,
    "categories": {}
}

for file_name in os.listdir(FAILURES_DIR):

    if file_name.endswith(".json"):

        file_path = os.path.join(FAILURES_DIR, file_name)

        with open(file_path) as f:
            failure = json.load(f)

        print(f"\nProcessing: {file_name}")

        prompt = build_prompt(failure)

        response = ask_ai(prompt, failure)

        response_data = json.loads(response)

        print(json.dumps(response_data, indent=4))

        save_report(response_data, file_name)

        # Update summary
        summary["total_failures"] += 1

        category = response_data["category"]

        if category not in summary["categories"]:
            summary["categories"][category] = 0

        summary["categories"][category] += 1

print("\n===== TRIAGE SUMMARY =====\n")
print(json.dumps(summary, indent=4))