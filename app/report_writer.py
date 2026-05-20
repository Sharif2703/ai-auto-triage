import json
from datetime import datetime

def save_report(response_data, original_file_name):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    clean_name = original_file_name.replace(".json", "")

    filename = f"../reports/{clean_name}_{timestamp}.json"

    with open(filename, "w") as report_file:
        json.dump(response_data, report_file, indent=4)

    print(f"\nReport saved: {filename}")