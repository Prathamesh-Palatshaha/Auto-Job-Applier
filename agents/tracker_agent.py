import json
from datetime import datetime
from state import JobApplicationState

def tracker_agent(state: JobApplicationState) -> JobApplicationState:

    log = {
        "company": state["selected_job"]["company"],
        "title": state["selected_job"]["title"],
        "score": state["match_score"],
        "approved": state["human_approval"],
        "timestamp": str(datetime.now())
    }

    with open("applications_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

    return state