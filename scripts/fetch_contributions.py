import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

USERNAME = "smithaum"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for day in soup.select("td.ContributionCalendar-day"):

    date = day.get("data-date")
    count = int(day.get("data-level", 0))
    level = int(day.get("data-level", 0))

    days.append({
        "date": date,
        "count": count,
        "level": level
    })

Path("data").mkdir(exist_ok=True)

with open("data/contributions.json", "w") as f:
    json.dump(days, f, indent=4)

print(f"Found {len(days)} days")