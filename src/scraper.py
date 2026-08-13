import requests
import pandas as pd
from datetime import datetime 

URL = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
response.encoding = "utf-8"
data = response.json()

def fix_text(text):
    if not isinstance(text, str):
        return text

    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

# Remove non-job records
jobs = [
    job for job in data
    if isinstance(job, dict) and "position" in job
]

# Select the fields we need
records = []

for job in jobs:
    records.append({
        "job_title": fix_text(job.get("position")),
        "company": fix_text(job.get("company")),
        "location": fix_text(job.get("location")),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "skills": job.get("tags"),
        "date": job.get("date"),
        "description": fix_text(job.get("description")),
        "url": job.get("url")
    })

df = pd.DataFrame(records)
# Add scraping timestamp
df["scraped_at"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

print("Number of jobs:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 jobs:")
print(df.head())

print("\nDataFrame information:")
print(df.info())

# Save raw scraped data
df.to_csv(
    "data/raw_jobs.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nRaw data saved successfully!")
print("File: data/raw_jobs.csv")