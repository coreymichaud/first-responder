# Frequently Asked Questions

Will admit these are not frequently asked... they're more so in case you're wondering about my decisions for parts of this project.

## Why Neon?
Originally I was using a local SQLite database to hold the companies and found jobs, however it meant that in order for this to work with GitHub Actions, I would need the database committed. That means the repo will look more like it's for me, and seem harder for others to use.

Once I switched to Neon, I was amazed! It took maybe 3 minutes from account creation to tables made with all my database information in it. I also really like that you can write SQL right in the console, and you can see and add rows to the tables. It's made it so it's way easier to insert 1 new company into the table.

## Why is it so hard to add new jobs?
I believe it's not technically hard to add a new job, as long as it's from Workday, Ashby, or Greenhouse. I am trying to make it so that if I find a careers page, other people can use it easier. For instance, right now it works by needing parameters in the URL unless it's a custom site. I'm working on it!

## Why Discord?
Originally I wanted to use Twilio to send texts when it finds a job, but I realized that it would be annoying to get lots of texts all day and it would cost money. The Discord webhook is free and easy to set up, so I chose it for the notifications.

## Why so much configuring?
Right now you need to find the companies, add to the database, change the code to match your own filters, and create your own scrapers for custom sites. As a result, it is a little bit time consuming, but I think it's worth it in the end. I'm trying to make it so that there is less to do.