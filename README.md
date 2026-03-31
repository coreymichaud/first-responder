# First Responder 🚑

Get job listings **fast** before everyone else does.

First Responder is a lightweight job scraper that monitors company career pages and sends **filtered, relevant job postings** directly to your Discord server.

## Features

* Scrapes jobs from:

  * Workday
  * Ashby
  * Greenhouse
  * Hacker News
  * Custom career pages
* Keyword-based filtering (allow / deny lists)
* Deduplicates jobs using a database
* Fully automated with GitHub Actions
* Discord webhook integration

## Tech Stack

* Python
* Playwright (Web scraping)
* PostgreSQL (Neon)
* GitHub Actions (CI/CD)

---

## Quick Start

### 1. Fork & Clone

Fork this repo, then clone your fork.

### 2. Rename Files

```bash
git mv .env.example .env
git mv markdown/COMPANIES_TEMPLATE.md markdown/COMPANIES.md
```

### 3. Setup Database ([Neon](https://neon.com))

Run the following SQL:

```sql
CREATE TABLE companies (
    company TEXT NOT NULL,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    UNIQUE(company, link, type)
);

CREATE TABLE seen (
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    date TEXT NOT NULL,
    UNIQUE(company, title, link, date)
);
```

### 4. Setup Discord Webhook

* Create a channel (e.g. `first-responder`)
* Create a webhook

### 5. Add Environment Variables

Add to the `.env` file:

```env
DISCORD_WEBHOOK = ""
DATABASE_URL = ""
```

Do the same for GitHub Action Secrets:

```env
DISCORD_WEBHOOK
DATABASE_URL
```

### 6. Run Locally

```bash
uv sync
uv run playwright install
uv run main.py
```

---

## Filtering Jobs

Edit:

```
filter/filters.py
```

* `allow`: job keywords you want
* `deny`: job keywords you don’t want

> Tip: include variations like `junior`, `jr`, `jr.`

## Adding Companies

Use `markdown/COMPANIES.md` to track company career pages.

Quick ways to find them:

* Workday → `site:wd1.myworkdayjobs.com`
* Ashby → `site:jobs.ashbyhq.com`
* Greenhouse → `site:job-boards.greenhouse.io`

You can bulk insert using a generated SQL statement, or add them one by one in the Neon console.

> Tip: I suggest using this file to make a big list first, bulk insert into the Neon database, then use it to keep a local track of companies and add new ones directly in the Neon console.

---

## Future Plans

* Smarter filtering using an LLM (job description matching)
* SMS notifications (Twilio)
* Local-first mode (local LLM + database)