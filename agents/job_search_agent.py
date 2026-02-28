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
        roles_ = ['Machine Learning Internship', 'AI intern', 'generative ai intern','data science internship']
        for role in roles_:
            querystring["query"] = role
            response = requests.get(url, headers=headers, params=querystring, timeout=60)
            response.raise_for_status()
            data = response.json()

        jobs = []

        # JSearch returns the results inside a 'data' array
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("job_title", ""),
                "company": item.get("employer_name", ""),
                "description": item.get("job_description", ""),
                "apply_link": item.get("job_apply_link", ""),
                "posted_date": item.get("job_posted_at_datetime_utc", "")
            })

        state["jobs"] = jobs
        
    except requests.exceptions.RequestException as e:
        print(f"[!] API Request failed: {e}")
        # Initialize as empty to prevent downstream errors in your graph
        state["jobs"] = [] 

    return state