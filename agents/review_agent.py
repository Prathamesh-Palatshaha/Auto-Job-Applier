from state import JobApplicationState

def review_agent(state: JobApplicationState) -> JobApplicationState:

    print("\n==============================")
    print("REVIEW JOB")
    print("==============================")

    job = state["selected_job"]

    print("Company:", job.get("company"))
    print("Title:", job.get("title"))
    print("Score:", state.get("match_score"))

    # Safe access
    if "evaluation_reasoning" in state:
        print(f"Reason for the job selection: {state['evaluation_reasoning']}")

    print("Apply Link:", job.get("apply_link"))
    print("==============================")

    decision = input("Approve application? (yes/no): ")

    if decision.lower() == "yes":
        state["human_approval"] = "approved"
    else:
        state["human_approval"] = "rejected"

    return state