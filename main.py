import os
from dotenv import load_dotenv
from notifier.discord import notify
from scrapers import workday, ashby, greenhouse
from database import create_db

# import importlib
import psycopg
import time
import datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

start_time = time.perf_counter()

if not os.path.exists("database/JOBS.db"):
    create_db()

con = psycopg.connect(DATABASE_URL)
cursor = con.cursor()

seen_available = True

try:
    cursor.execute('DELETE FROM seen WHERE "date"::date < CURRENT_DATE - INTERVAL \'2 months\'')
    cursor.execute("SELECT company, title, link FROM seen")
    seen_rows = cursor.fetchall()
    seen_keys = {(company, title, link) for company, title, link in seen_rows}
except psycopg.OperationalError:
    seen_available = False
    seen_keys = set()

cursor.execute("SELECT * FROM companies")

rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]

companies = [dict(zip(column_names, row)) for row in rows]
# companies = companies[0:1]

print("[START] Beginning job scraper.")

found_jobs = []

for company in companies:
    if company["type"] == "workday":
        temp = workday.scrape(company["company"], company["link"])
    elif company["type"] == "ashby":
        temp = ashby.scrape(company["company"], company["link"])
    elif company["type"] == "greenhouse":
        temp = greenhouse.scrape(company["company"], company["link"])
    elif company["type"] == "hackernews":
        continue
    elif company["type"] == "custom":
        continue
        # module_name = company["company"].lower().replace(" ", "_")
        # module = importlib.import_module(f"scrapers.custom.{module_name}")
        # temp = module.scrape(company["company"], company["link"])

    found_jobs = found_jobs + temp

today = datetime.date.today().isoformat()
if not seen_available:
    new_jobs = found_jobs
else:
    new_jobs = []
    for job in found_jobs:
        key = (job["company"], job["title"], job["link"])
        if key in seen_keys:
            continue

        new_jobs.append(job)
        cursor.execute(
            'INSERT INTO seen (company, title, link, date) VALUES (%s, %s, %s, %s)',
            (job["company"], job["title"], job["link"], today),
        )
        seen_keys.add(key)

con.commit()
con.close()

notify(new_jobs)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"[TIME] Ran in {elapsed_time:.2f} seconds.")
print("[DONE] Ending job scraper.")
