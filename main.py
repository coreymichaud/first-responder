import os
import asyncio
import datetime
import time
import psycopg
from dotenv import load_dotenv
from scrapers import workday, ashby, greenhouse
from notifier.discord import notify
from playwright.async_api import async_playwright

load_dotenv()

SCRAPER_MAP = {
    "workday": workday.scrape,
    "ashby": ashby.scrape,
    "greenhouse": greenhouse.scrape,
}

SEMAPHORE = asyncio.Semaphore(4)


async def run_scraper(scraper, company_name, link, context):
    async with SEMAPHORE:
        return await scraper(company_name, link, context)


async def gather_all_jobs(companies):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        tasks = [
            asyncio.create_task(
                run_scraper(
                    SCRAPER_MAP[c["platform"]], c["company"], c["link"], context
                )
            )
            for c in companies
            if c["platform"] in SCRAPER_MAP
        ]

        if not tasks:
            return []

        found = []
        for res in await asyncio.gather(*tasks, return_exceptions=True):
            if isinstance(res, Exception):
                print(f"[ERROR] Scraper failed: {res}")
            elif isinstance(res, list):
                found.extend(res)
            else:
                print(f"[WARN] Unexpected scraper return type: {type(res)}")
        return found

    await context.close()
    await browser.close()


async def main():
    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        con = psycopg.connect(DATABASE_URL, row_factory=psycopg.rows.dict_row)
        cursor = con.cursor()
        cursor.execute(
            "DELETE FROM seen WHERE \"date\"::date < CURRENT_DATE - INTERVAL '2 months'"
        )
        cursor.execute("SELECT company, title, link FROM seen")
        seen_keys = {(r["company"], r["title"], r["link"]) for r in cursor.fetchall()}
        cursor.execute("SELECT * FROM companies")
        companies = cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        exit(1)

    found_jobs = await gather_all_jobs(companies)

    new_jobs = [
        job
        for job in found_jobs
        if (job["company"], job["title"], job["link"]) not in seen_keys
    ]

    if new_jobs:
        today = datetime.date.today().isoformat()
        cursor.executemany(
            "INSERT INTO seen (company, title, link, date) VALUES (%s, %s, %s, %s)",
            [(j["company"], j["title"], j["link"], today) for j in new_jobs],
        )
        con.commit()

    con.close()
    notify(new_jobs)


if __name__ == "__main__":
    print("[START] Beginning scraper.")
    start = time.perf_counter()
    asyncio.run(main())
    print(f"[TIME] Ran in {time.perf_counter() - start:.2f} seconds.")
    print("[DONE] Ending scraper.")
