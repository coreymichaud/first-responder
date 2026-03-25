# =================================================================
# This script is for the custom logic to scrape jobs on Greenhouse.
# =================================================================

from playwright.sync_api import sync_playwright, TimeoutError
from filter.filters import filter_title


def scrape(company: str, link: str) -> list:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        print(f"[INFO] Scraping {company}.")

        try:
            page = context.new_page()
            page.goto(link, wait_until="domcontentloaded", timeout=6000)
            page.wait_for_selector(".job-post", timeout=6000)

            jobs_locator = page.locator(".job-post")

            titles = [
                el.locator("p.body--medium").inner_text() for el in jobs_locator.all()
            ]
            locations = [
                el.locator("p.body--metadata").inner_text() for el in jobs_locator.all()
            ]
            links = [el.locator("a").get_attribute("href") for el in jobs_locator.all()]

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
#     "GitLab",
#     "https://job-boards.greenhouse.io/gitlab?departments%5B%5D=4115238002&departments%5B%5D=4115239002&departments%5B%5D=4118835002&departments%5B%5D=4069215002&departments%5B%5D=4115236002",
# )
# print(testing)
