# =============================================================
# This script is for the custom logic to scrape jobs on Ashby.
# =============================================================

from playwright.sync_api import sync_playwright, TimeoutError
from filter.filters import filter_title


def scrape(company: str, link: str) -> list:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        print(f"[INFO] Scraping {company}.")

        try:
            page = context.new_page()
            page.goto(link, wait_until="domcontentloaded")

            try:
                page.wait_for_selector(
                    ".ashby-job-posting-brief-list > a", timeout=4000
                )
            except:
                page.reload(wait_until="domcontentloaded")
                page.wait_for_selector(
                    ".ashby-job-posting-brief-list > a", timeout=4000
                )

            jobs_locator = page.locator(".ashby-job-posting-brief-list > a")

            titles = [
                el.locator(".ashby-job-posting-brief-title").inner_text()
                for el in jobs_locator.all()
            ]
            locations = [
                el.locator(
                    ".ashby-job-posting-brief-details p:first-of-type"
                ).inner_text()
                for el in jobs_locator.all()
            ]
            links = [
                "https://jobs.ashbyhq.com" + el.get_attribute("href")
                for el in jobs_locator.all()
            ]

            jobs = [
                {"title": t, "company": company, "location": loc, "link": l}
                for t, loc, l in zip(titles, locations, links)
                if filter_title(t)
            ]

        except TimeoutError:
            print(f"[SKIP] {company} timed out — skipping.")
            jobs = []

        finally:
            context.close()
            browser.close()

    return jobs


# testing = scrape(
#     "Clay",
#     "https://jobs.ashbyhq.com/claylabs?employmentType=FullTime&locationId=f62b23aa-31f0-4374-b447-18c02444108f",
# )
# print(testing)
