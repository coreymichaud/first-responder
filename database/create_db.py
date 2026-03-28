# ======================================================================================================
# This script creates the database jobs.db with the tables `companies` and `seen`.
# If you have data in these tables and run this script again, it will overwrite them when OVERWRITE = 1.
# ======================================================================================================

import sqlite3

OVERWRITE = 0

if OVERWRITE:
    con = sqlite3.connect("database/JOBS.db")
    cur = con.cursor()

    cur.execute("""
            CREATE TABLE companies (
                company TEXT NOT NULL,
                link TEXT NOT NULL,
                type TEXT NOT NULL,
                UNIQUE(company, link, type));
    """)

    cur.execute("""
            CREATE TABLE seen (
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                date TEXT NOT NULL,
                UNIQUE(company, title, link, date));
    """)

    con.close()
