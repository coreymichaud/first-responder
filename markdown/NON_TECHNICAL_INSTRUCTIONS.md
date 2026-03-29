# Was that confusing?
Sorry! I wanted to make the [README](../README.md) as indepth as I could, then I realized I wrote a very long and verbose set of instructions so it didn't seem very good for technical users who want the TL;DR. This markdown file acts as that long and verbose set of instructions to make sure you understand how to use First Responder from a non-technical standpoint!

Besides the instructions below, I did not include the introduction to this project or "What's next?" like I did in the [README](../README.md), so if you would still like to read those, go check them out!

# Some pre-setup setup
Before continuing onto the setup, you want to make sure you understand everything that is going to be said! As a quick note, anytime you see a command block:
```{bash}
Like this!
```
then you should copy what it shows exactly so you don't make any typos.

Let's get into it!

## Terminal
The terminal is an application on your computer that you can use to interact with files. Find the terminal on your computer and open it up.

## Install git
Once the terminal is open, enter the command:
```{git}
git -v
```

If you do not see a version printed, then you do not have git installed. If you're on Windows, go to the [git installation for Windows](https://git-scm.com/install/windows) website and download git. If you're on Mac and somehow do not have git installed, you most likely don't have Xcode or brew installed. I would suggest running the command:
```{bash}
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
which installs Homebrew, and then:
```{bash}
brew install git
```
to install git.

Now run the git version command from earlier to see if it shows a version. If it does, let's continue!

## Install Python
To see if you have Python installed, run the command:
```{bash}
python3 -V
```

If you do not see a version printed, go to the [Python download](https://www.python.org/downloads/) website and download the latest version of python. Then run that Python version command again and see if it works.

## Install UV
Once you have Python installed, you also have Python's package manager `pip`.

Run this command to install `uv`:
```{bash}
pip install uv
```
and if it doesn't work, replace `pip` with `pip3`. If once again that doesn't work, add `python3` in front of it.

## Create a GitHub account if you don't already have one
- Create GH account

## Fork repository
- Show how to fork and clone to local computer

# Setup
Before setting up the environment variables, let's first change some of the file names.

Let's change the file name of `.env.example` to `.env`
```{bash}
git mv .env.example .env
```
and then change the file name of `COMPANIES_TEMPLATE.md` to `COMPANIES.md`
```{bash}
git mv markdown/COMPANIES_TEMPLATE.md markdown/COMPANIES.md
```

What is this `COMPANIES.md` file? Use it or don't use it, it's up to you, but it is where you can keep a quick and easy list of companies and their career page URL so you can keep track of it. More importantly, I'm assuming if you're reading this then you do not have a list of companies with their exact careers links ready to go. If you spend some time making a big list of companies and their links, you can add it to that file and use it to put all the information into the database at once (more information on that later).

To find these companies, you can enter the following `site:` into a search engine to find all links that match the careers page. This is best for the job boards, but not custom scrapers (the companies that do not use a dedicated job board like greenhouse or ashby).
- **Workday:** site:wd1.myworkdayjobs.com
- **Ashby:** site:jobs.ashbyhq.com
- **Greenhouse:** site:job-boards.greenhouse.io

## Discord Webhook
On a Discord server you'd like to use (I'd suggest creating one for this project if you don't have one available), create a new channel called `first-responder` and create a new webhook named "First Responder". If you don't know how to do this, follow this order after creating a channel:
- Edit Channel (gear icon) -> Integrations -> Webhooks -> New Webhook -> Click on new webhook

Once you have the webhook URL copied, go into your `.env` file and and add it to `DISCORD_WEBHOOK`. Then, after creating a GitHub repo for your clone (maybe best option is to fork this repo for ease of use), add this as a GitHub Actions Secret. If you don't know how to do this, follow this order once you've set up your repository:
- Settings -> Secrets and variables -> Actions -> New repository secret -> then "Name" should be "DISCORD_WEBHOOK" and the "Secret" should be your copied Discord webhook URL.

## Neon PostgreSQL Database
If you don't already have a [Neon](https://neon.com) account, go ahead and create one. For this project, the free trial will be enough, and we will use this for serverless PostgreSQL.

Once you have an account, create a new project and add the connection string to your `.env` file for the `DATABASE_URL` variable. If you don't know how to set up a project on Neon and get this connection string, follow this order after having an account:
- New Project -> type "First Responder" for Project name -> Create -> Connection string -> then press the "copy snippet" button below the connection string.

Set up the GitHub Actions Secret the same way you did for Discord, where the "Name" is "DATABASE_URL" and the "Secret" is that connection string.

After setting up the project, go into the "SQL Editor" tab on the left and run the following SQL statements separately.

To create the table `companies` run
```{SQL}
CREATE TABLE companies (
    company TEXT NOT NULL,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    UNIQUE(company, link, type)
);
```

To create the table `seen` run
```{SQL}
CREATE TABLE seen (
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    date TEXT NOT NULL,
    UNIQUE(company, title, link, date)
);
```

Do you remember that `COMPANIES.md` file from earlier? If you fill out that file with companies, you can ask AI the follow prompt to get a PostgreSQL statement to insert the massive list of companies into the `companies` table all at once on Neon.
```{prompt}
Using the attached COMPANIES.md, give me a single PostgreSQL INSERT statement that inserts all companies into a table called companies with columns company, link, and type (which is the job board: workday, ashby, greenhouse, hackernews, or custom).
```

Neon is great because after we have our 2 tables filled, we can view the tables directly online without needing to install any database software like pgAdmin. You can also very easily add one-off companies to the list if you find one later on.

# Running the scraper
- Once everything is set up (Discord webhook on a channel, Neon connection string with a project, Postgres tables set up, GH actions secrets set up, all modified code in your repo) you can now run the scraper locally to test it out!

In the project directory run
```{bash}
uv sync
```
then
```{bash}
uv run playwright install
```
and finally
```{bash}
uv run main.py
```