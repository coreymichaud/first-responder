# Greenhouse

from playwright.async_api import async_playwright, TimeoutError
from filter.filters import filter_title


async def scrape(company: str, link: str, context) -> list:
    print(f"[INFO] Scraping {company}.")

    try:
        page = await context.new_page()
        await page.goto(link, wait_until="domcontentloaded")

        try:
            await page.wait_for_selector(".job-post", timeout=4000)
        except:
            await page.reload(wait_until="domcontentloaded")
            await page.wait_for_selector(".job-post", timeout=4000)

        jobs_locator = page.locator(".job-post")

        titles = await jobs_locator.locator("p.body--medium").all_inner_texts()
        links = await jobs_locator.evaluate_all(
            "elements => elements.map(el => { const a = el.querySelector('a'); return a ? a.href : null; })"
        )

        jobs = [
            {"title": t, "company": company, "link": l}
            for t, l in zip(titles, links)
            if filter_title(t)
        ]

    except TimeoutError:
        print(f"[SKIP] {company} timed out — skipping.")
        jobs = []

    return jobs
