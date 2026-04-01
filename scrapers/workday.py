# ===============================================================
# This script is for the custom logic to scrape jobs on Workday.
# ===============================================================

from playwright.async_api import async_playwright, TimeoutError
from filter.filters import filter_title


async def scrape(company: str, link: str) -> list:

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        print(f"[INFO] Scraping {company}.")

        try:
            page = await context.new_page()
            await page.goto(link, wait_until="domcontentloaded")

            try:
                await page.wait_for_selector(
                    'a[data-automation-id="jobTitle"]', timeout=4000
                )
            except:
                await page.reload(wait_until="domcontentloaded")
                await page.wait_for_selector(
                    'a[data-automation-id="jobTitle"]', timeout=4000
                )

            jobs_locator = page.locator('a[data-automation-id="jobTitle"]')

            titles = await jobs_locator.all_inner_texts()
            locations = await page.locator(
                '[data-automation-id="locations"] dd'
            ).all_inner_texts()
            links = await jobs_locator.evaluate_all(
                "elements => elements.map(el => el.href)"
            )

            jobs = [
                {"title": t, "company": company, "location": loc, "link": l}
                for t, loc, l in zip(titles, locations, links)
                if filter_title(t)
            ]

        except TimeoutError:
            print(f"[SKIP] {company} timed out — skipping.")
            jobs = []

        finally:
            await context.close()
            await browser.close()

    return jobs
