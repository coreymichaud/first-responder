# Ashby

from playwright.async_api import async_playwright, TimeoutError
from filter.filters import filter_title


async def scrape(company: str, link: str, context) -> list:
    print(f"[INFO] Scraping {company}.")

    try:
        page = await context.new_page()
        await page.goto(link, wait_until="domcontentloaded")

        try:
            await page.wait_for_selector(
                ".ashby-job-posting-brief-list > a", timeout=4000
            )
        except:
            await page.reload(wait_until="domcontentloaded")
            await page.wait_for_selector(
                ".ashby-job-posting-brief-list > a", timeout=4000
            )

        jobs_locator = page.locator(".ashby-job-posting-brief-list > a")

        titles = await jobs_locator.locator(
            ".ashby-job-posting-brief-title"
        ).all_inner_texts()
        locations = await jobs_locator.locator(
            ".ashby-job-posting-brief-details p:first-of-type"
        ).all_inner_texts()
        links = await jobs_locator.evaluate_all(
            "elements => elements.map(el => 'https://jobs.ashbyhq.com' + (el.getAttribute('href') || ''))"
        )

        jobs = [
            {"title": t, "company": company, "location": loc, "link": l}
            for t, loc, l in zip(titles, locations, links)
            if filter_title(t)
        ]

    except TimeoutError:
        print(f"[SKIP] {company} timed out — skipping.")
        jobs = []

    return jobs
