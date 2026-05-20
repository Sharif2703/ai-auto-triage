import json
import re

def ask_ai(prompt, failure_data):

    exception_type = failure_data.get("exception_type", "")
    logs = failure_data.get("logs_tail", "")
    http_errors = failure_data.get("http_errors", "")
    stack_trace = failure_data.get("stack_trace", "")
    history = failure_data.get("history", [])

    category = "UNKNOWN"
    root_cause = "Unable to determine"
    owner = "QA Team"
    confidence = "LOW"

    detected_patterns = []

    # =========================
    # REGEX PATTERN DETECTION
    # =========================

    if re.search(r"timeout", logs, re.IGNORECASE):
        detected_patterns.append("TIMEOUT_DETECTED")

    if re.search(r"locator|element not found", logs, re.IGNORECASE):
        detected_patterns.append("LOCATOR_ISSUE")

    if re.search(r"500|503|404", http_errors):
        detected_patterns.append("HTTP_ERROR")

    if re.search(r"assert", stack_trace, re.IGNORECASE):
        detected_patterns.append("ASSERTION_FAILURE")

    # =========================
    # FLAKY TEST DETECTION
    # =========================

    pass_count = history.count("PASS")
    fail_count = history.count("FAIL")

    flaky_score = 0
    flaky_test = False

    if len(history) >= 4 and pass_count > 0 and fail_count > 0:
        flaky_test = True
        flaky_score = int((fail_count / len(history)) * 100)

    # =========================
    # DECISION LOGIC
    # =========================

    if flaky_test:
        category = "FLAKY_TEST"
        root_cause = "Intermittent test behavior detected"
        owner = "Automation QA Team"
        confidence = "MEDIUM"

    elif "HTTP_ERROR" in detected_patterns:
        category = "API_FAILURE"
        root_cause = f"Backend/API issue detected: {http_errors}"
        owner = "Backend API Team"
        confidence = "HIGH"

    elif "LOCATOR_ISSUE" in detected_patterns:
        category = "LOCATOR_FAILURE"
        root_cause = "UI locator likely changed or element unavailable"
        owner = "Automation QA Team"
        confidence = "HIGH"

    elif "ASSERTION_FAILURE" in detected_patterns:
        category = "ASSERTION_FAILURE"
        root_cause = "Validation/assertion failed during test"
        owner = "Test Automation Team"
        confidence = "MEDIUM"

    elif "TIMEOUT_DETECTED" in detected_patterns:
        category = "TIMEOUT_FAILURE"
        root_cause = "Operation exceeded allowed timeout"
        owner = "Infra or Automation Team"
        confidence = "MEDIUM"

    response = {
        "category": category,
        "root_cause": root_cause,
        "owner": owner,
        "confidence": confidence,
        "detected_patterns": detected_patterns,
        "history": history,
        "flaky_test": flaky_test,
        "flaky_score": flaky_score
    }

    return json.dumps(response, indent=4)