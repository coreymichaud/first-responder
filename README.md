# 🚑 First Responder

Get job listings **fast** before everyone else does.

First Responder is a lightweight job scraper that monitors company career pages and sends **filtered, relevant job postings** directly to your Discord server.

---

## ✨ Why This Exists

Job searching is noisy and slow. First Responder flips that:

* ⚡ Scrapes jobs automatically (every 2 hours via GitHub Actions)
* 🎯 Filters roles based on your preferences
* 🔔 Sends results instantly to Discord

## 🚀 Features

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

## 🧱 Tech Stack

* Python
* Playwright
* PostgreSQL (Neon)
* GitHub Actions (CI/CD)

## ⚡ Quick Start

If you're non-technical or get confused at any point, check out the [non-technical guide](markdown/NON_TECHNICAL_INSTRUCTIONS.md)!

### 1. Fork & Clone

Fork this repo, then clone your fork.

### 2. Setup Environment

```bash
git mv .env.example .env
git mv markdown/COMPANIES_TEMPLATE.md markdown/COMPANIES.md
```

Fill in `.env`:

```env
DISCORD_WEBHOOK=your_webhook_url
DATABASE_URL=your_database_url
```

### 3. Setup Database (Neon)

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
* Paste it into `.env` and GitHub Secrets

### 5. Run Locally

```bash
uv sync
uv run playwright install
uv run main.py
```

---

## 🎯 Filtering Jobs

Edit:

```
filter/filters.py
```

* `allow`: jobs you want
* `deny`: jobs you don’t want

> Tip: include variations like `junior`, `jr`, `jr.`

## 🏢 Adding Companies

Use `markdown/COMPANIES.md` to track company career pages.

Quick ways to find them:

* Workday → `site:wd1.myworkdayjobs.com`
* Ashby → `site:jobs.ashbyhq.com`
* Greenhouse → `site:job-boards.greenhouse.io`

You can bulk insert using a generated SQL statement from this file, or add them one by one in the Neon console.

## 🔄 Automation

GitHub Actions runs the scraper every 2 hours.

Make sure to set secrets:

* `DISCORD_WEBHOOK`
* `DATABASE_URL`

---

## 🗺️ Future Plans

* 🤖 Smarter filtering using an LLM (job description matching)
* 📱 SMS notifications (Twilio)
* 🏠 Local-first mode (local LLM + database)

## ⭐ If You Like This Project

Give it a star and consider contributing!