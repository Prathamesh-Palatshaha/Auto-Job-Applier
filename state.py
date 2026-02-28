from typing import TypedDict, List, Dict, Any

class JobApplicationState(TypedDict):
    resume_paths: List[str]
    resumes: List[Dict[str, Any]]
    jobs: List[Dict[str, Any]]

    selected_job: Dict[str, Any]
    selected_resume: Dict[str, Any]
    match_score: float
    evaluation_reasoning: str
    decision: str
    human_approval: str