def calculate_score(execution_results, log_results):

    score = 50  # Start from neutral baseline

    report = {
        "network_exposure": None,
        "execution_control": None,
        "detection_visibility": None,
        "final_score": 0,
        "security_rating": None
    }

    # -----------------------------
    # Network Exposure Assessment
    # -----------------------------
    if execution_results.get("network_reachable"):
        score -= 10
        report["network_exposure"] = "WinRM service exposed"
    else:
        score += 10
        report["network_exposure"] = "WinRM not reachable"

    # -----------------------------
    # Authentication Check
    # -----------------------------
    if execution_results.get("authentication_success"):
        score -= 15
    else:
        score += 15

    # -----------------------------
    # Execution Control
    # -----------------------------
    if execution_results.get("execution_success"):
        score -= 25
        report["execution_control"] = "Remote execution allowed"
    else:
        score += 25
        report["execution_control"] = "Execution blocked"

    # -----------------------------
    # Detection Visibility
    # -----------------------------
    if log_results.get("defender_events_found"):
        score += 25

    if log_results.get("powershell_events_found"):
        score += 15

    # Normalize score
    if score > 100:
        score = 100
    if score < 0:
        score = 0

    report["final_score"] = score

    # -----------------------------
    # Security Rating Classification
    # -----------------------------
    if score >= 80:
        report["security_rating"] = "STRONG"
    elif score >= 60:
        report["security_rating"] = "MODERATE"
    elif score >= 40:
        report["security_rating"] = "WEAK"
    else:
        report["security_rating"] = "CRITICAL"

    return report
