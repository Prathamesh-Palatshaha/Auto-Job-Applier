import os
import requests
from state import JobApplicationState

def job_search_agent(state: JobApplicationState) -> JobApplicationState:
    # Swapped to JSearch API (available on RapidAPI) for reliable job data
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query":"Machine Learning Internship",
                   "page":"1","num_pages":"1",
                   "language":"english",
                   "date_posted":"today",
                   "work_from_home":"true",
                   "job_requirements":"no_experience"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        all_responses = []
        roles_ = ['Machine Learning Internship', 'AI intern', 'generative ai intern', 'data science internship']
        
        for role in roles_:
            querystring["query"] = role
            try:
                response = requests.get(url, headers=headers, params=querystring, timeout=60)
                response.raise_for_status()
                all_responses.append(response.json())
            except requests.exceptions.RequestException as e:
                print(f"[!] Failed to fetch jobs for '{role}': {e}")
                continue  # Skip this role and try the next one

        jobs = []

        # JSearch returns the results inside a 'data' array
        for response_data in all_responses:
            for job_item in response_data.get("data", []):
                jobs.append({
                    "title": job_item.get("job_title", ""),
                    "company": job_item.get("employer_name", ""),
                    "description": job_item.get("job_description", ""),
                    "apply_link": job_item.get("job_apply_link", ""),
                    "posted_date": job_item.get("job_posted_at_datetime_utc", "")
                })

        state["jobs"] = jobs
        print(f"🔎 Total jobs fetched: {len(jobs)}")
    
    except Exception as e:
        print(f"[!] Critical error in job search: {e}")
        state["jobs"] = []

    return state