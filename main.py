from notifier.discord import notify
from scrapers import workday, ashby, greenhouse

# import importlib
import sqlite3
import time

start_time = time.perf_counter()

con = sqlite3.connect("database/JOBS.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM companies")

rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]

con.close()

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
    else:
        continue
        # module_name = company["company"].lower().replace(" ", "_")
        # module = importlib.import_module(f"scrapers.custom.{module_name}")
        # temp = module.scrape(company["company"], company["link"])

    found_jobs = found_jobs + temp

notify(found_jobs)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"[TIME] Ran in {elapsed_time:.2f} seconds.")
print("[DONE] Ending job scraper.")
