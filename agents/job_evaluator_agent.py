import os
import json
import google.generativeai as genai
from state import JobApplicationState

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

def job_evaluator_agent(state: JobApplicationState) -> JobApplicationState:
    resumes = state.get("resumes", [])

    for job in state.get("jobs", []):
        prompt = f"""
        You are an expert technical recruiter and a highly precise Applicant Tracking System (ATS).
        Your task is to evaluate a list of candidate resumes against a specific job posting to find the best match.

        EVALUATION CRITERIA:
        1. Extract the core skills, required experience level, and key responsibilities from the Job Posting.
        2. Analyze each resume to see how well it aligns with those requirements.
        3. Assign a match score between 0.0 and 1.0 to the best-fitting resume (e.g., 0.85).
        4. If the best score is >= 0.60, set the decision to "apply". Otherwise, set it to "skip".

        Resumes (Array):
        {json.dumps(resumes, indent=2)}

        Job Posting:
        {json.dumps(job, indent=2)}

        Respond using this exact JSON schema:
        {{
          "reasoning": "Briefly explain why this resume was chosen and justify the match score.",
          "selected_resume_index": <int, the 0-based array index of the chosen resume>,
          "score": <float, between 0.0 and 1.0>,
          "decision": "apply" or "skip"
        }}
        """

        try:
            # Enforce JSON output natively and lower temperature for analytical consistency
            response = model.generate_content(prompt)
            response_text = response.text.strip()

            # Remove markdown if wrapped
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]

            result = json.loads(response_text)

            # Check the conditions and safely get dictionary values
            if result.get("decision") == "apply" and result.get("score", 0.0) >= 0.60:
                state["selected_job"] = job
                
                # Ensure the index is within bounds to prevent IndexError
                idx = result.get("selected_resume_index", 0)
                if resumes and 0 <= idx < len(resumes):
                    state["selected_resume"] = resumes[idx]
                elif resumes:
                    state["selected_resume"] = resumes[0]
                else:
                    print("[!] No resumes available to select!")
                    state["decision"] = "skip"
                    return state
                
                state["match_score"] = result.get("score")
                state["decision"] = "apply"
                state["evaluation_reasoning"] = result.get("reasoning")
                return state

        except Exception as e:
            print(f"[!] Evaluation failed for job {job.get('title', 'Unknown')}: {e}")
            continue # If parsing or API fails, safely skip to the next job

    # If loop completes without finding a match >= 0.75
    state["decision"] = "skip"
    return state