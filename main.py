import os
from dotenv import load_dotenv
from notifier.discord import notify
from scrapers import workday, ashby, greenhouse
import asyncio
import inspect

# import importlib
import psycopg
import time
import datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

start_time = time.perf_counter()

with psycopg.connect(DATABASE_URL) as con:
    with con.cursor() as cursor:
        seen_available = True

        try:
            cursor.execute(
                "DELETE FROM seen WHERE \"date\"::date < CURRENT_DATE - INTERVAL '2 months'"
            )
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


async def _run_scraper(func, company_name, link):
    """
    Call func(company_name, link).
    If func is async, await it. Otherwise run it in a thread.
    """
    if inspect.iscoroutinefunction(func):
        return await func(company_name, link)

    return await asyncio.to_thread(func, company_name, link)


SEMAPHORE = asyncio.Semaphore(4)

async def _bounded(coro):
    async with SEMAPHORE:
        return await coro

async def _gather_all_jobs(companies):
    tasks = []
    for company in companies:
        typ = company["type"]
        if typ == "workday":
            tasks.append(
                asyncio.create_task(
                    _bounded(_run_scraper(workday.scrape, company["company"], company["link"]))
                )
            )
        elif typ == "ashby":
            tasks.append(
                asyncio.create_task(
                    _bounded(_run_scraper(ashby.scrape, company["company"], company["link"]))
                )
            )
        elif typ == "greenhouse":
            tasks.append(
                asyncio.create_task(
                    _bounded(_run_scraper(greenhouse.scrape, company["company"], company["link"]))
                )
            )
        elif typ in ("hackernews", "custom"):
            # skip or implement custom handling
            continue

    if not tasks:
        return []

    results = await asyncio.gather(*tasks, return_exceptions=True)

    found = []
    for res in results:
        if isinstance(res, Exception):
            print(f"[ERROR] Scraper failed: {res}")
            continue
        if isinstance(res, list):
            found.extend(res)
        else:
            print(f"[WARN] Scraper returned unexpected type: {type(res)}")
    return found


async def main_async():
    found_jobs = await _gather_all_jobs(companies)

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
            seen_keys.add(key)

    if new_jobs:
        with psycopg.connect(DATABASE_URL) as con:
            with con.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO seen (company, title, link, date) VALUES (%s, %s, %s, %s)",
                    [(j["company"], j["title"], j["link"], today) for j in new_jobs],
                )

    notify(new_jobs)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"[TIME] Ran in {elapsed_time:.2f} seconds.")
    print("[DONE] Ending job scraper.")


if __name__ == "__main__":
    asyncio.run(main_async())
