import os
import requests

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def search_jobs_api(
    query="",
    location="",
    page=1,
    country="in",
    job_type="",
    min_salary=None,
):
    """
    Adzuna API se jobs fetch karta hai.
    Supports:
    - job title (query)
    - location
    - job type (full_time, part_time, contract)
    - minimum salary filter
    """

    url = f"{BASE_URL}/{country}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 15,
        "what": query,
        "where": location,
        "content-type": "application/json",
    }

    if min_salary:
        params["salary_min"] = min_salary

    if job_type:
        
        params["contract_time"] = job_type  

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Adzuna error:", response.status_code, response.text)
        return []

    data = response.json()
    return data.get("results", [])
