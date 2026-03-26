# ================================================================
# This script adds company data to the companies table in jobs.db.
# ================================================================

import sqlite3

con = sqlite3.connect("database/JOBS.db")
cursor = con.cursor()

COMPANY = ""
LINK = ""
TYPE = ""

# cursor.execute(
#     "INSERT INTO companies (company, link, type) VALUES (?, ?, ?)",
#     (COMPANY, LINK, TYPE),
# )

cursor.executescript("""""")

con.close()
