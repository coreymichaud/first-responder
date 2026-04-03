# Hacker News

# from playwright.async_api import async_playwright, TimeoutError


# async def scrape(company: str, link: str) -> list:

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context()

#         print(f"[INFO] Scraping {company}.")

#         try:
#             page = await context.new_page()
#             await page.goto("https://news.ycombinator.com/news", wait_until="domcontentloaded")

#             if await page.get_by_text("Who's Hiring?").count() == 1:
#                 link = await page.get_by_text("Who's Hiring?").evaluate("el => el.href")


#         except TimeoutError:
#             print(f"[SKIP] {company} timed out — skipping.")

#         finally:
#             await context.close()
#             await browser.close()
#
#     return []

# print(scrape("Hacker News", "https://news.ycombinator.com/item?id=47219668"))

# COREY!!! I need to take time to code this... but the idea is to go to the new.ycombinator site and see if there is a whos hiring thread. if there is, then set that as the link to use and replace the current link on the db with that one.
# Then go to the whos hiring thread and scrape the job posts. It should be that for each post, it will check if it has my keywords, and if it does then it will send it directly to discord with just the title and post, no link.
# In the main.py file, it should not add any of the jobs from hacker news to the "found_jobs" list, since they will be sent directly to discord. So the scraper for hacker news should return an empty list, and just send the jobs directly to discord as it finds them.
