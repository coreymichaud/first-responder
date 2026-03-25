- Talk about that this is currently fully tailored for me, and that in the future i'm going to try to make this where anyone can easily use it
- Talk about what prompt to ask AI with the JOBS.md file to get SQL to insert into the database and how to set up the JOBS.md (including how to find those jobs)
- Talk about how to set this up, like with the discord web hook and stuff
- Talk about not how the create_db.py file should be run first, then set OVERWRITE to 0 so it won't overwrite the db and that you can run it when downloading from discord so that you can clear the information i have in it

This is the prompt to get the companies into the database:
'''
Using the attached JOBS.md, give me a single SQLite INSERT statement that inserts all companies into a table called companies with columns company, link, and type (which is the job board: workday, ashby, greenhouse, or custom).
'''

- Talk about how this is currently fully tailored to yourself, but once you figure everything out (basically when it works for you the way you want it to) then you will modify the code to make it so other people can use it easier.