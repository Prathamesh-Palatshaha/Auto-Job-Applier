import os
from resume_parser import ResumeParser
from state import JobApplicationState


def resume_agent(state: JobApplicationState) -> JobApplicationState:
    api_key = os.getenv("GEMINI_API_KEY")
    # print("Loaded Gemini Key:", api_key)
    parser = ResumeParser(api_key)

    structured = []
    for path in state["resume_paths"]:
        parsed = parser.parse_resume(path)
        structured.append(parsed)

    state["resumes"] = structured
    return state