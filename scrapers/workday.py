# ===============================================================
# This script is for the custom logic to scrape jobs on Workday.
# ===============================================================

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
                page.wait_for_selector('a[data-automation-id="jobTitle"]', timeout=4000)
            except:
                page.reload(wait_until="domcontentloaded")
                page.wait_for_selector('a[data-automation-id="jobTitle"]', timeout=4000)

            jobs_locator = page.locator('a[data-automation-id="jobTitle"]')

            titles = jobs_locator.all_inner_texts()
            locations = page.locator(
                '[data-automation-id="locations"] dd'
            ).all_inner_texts()
            links = jobs_locator.evaluate_all("elements => elements.map(el => el.href)")

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
#     "Capital One",
#     "https://capitalone.wd12.myworkdayjobs.com/Capital_One/?locations=af51744fb4fc010ca9b81af56b6b0000&locations=3b0d3024e0af103d6c20dba04f9310e6&locations=5303cb0ddb47102d5fa0be27262f0227&locations=5303cb0ddb47102d5fa30ae341b60486&locations=5303cb0ddb47102d5fa910ad457f0722&locations=3b0d3024e0af103d6c1fe8eecb650f4b&locations=5303cb0ddb47102d5fa37e77cbf004fa&locations=5303cb0ddb47102d5fa152c296fe02b9&locations=5303cb0ddb47102d5fa2bff8ec720438&timeType=2ed180e199081055c65d9d6853aa022d&workerSubType=a12c70bf789e10572aab8e8909a619ae",
# )
# print(testing)
