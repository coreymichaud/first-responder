# =====================================================================================
# This script sets up the Discord webhook to send job postings to the Discord channel.
# =====================================================================================

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def notify(job_list: list) -> None:

    print(f"[DEBUG] Notification function received {len(job_list)} jobs.")

    if len(job_list) == 0:
        print("[SKIP] No jobs sent because no jobs found.")
    else:
        for job in job_list:
            requests.post(
                DISCORD_WEBHOOK,
                json={
                    "embeds": [
                        {
                            "title": f"🎯 New Job Found!",
                            "description": f"**{job['company']}**\n[{job['title']}]({job['link']})",
                        }
                    ]
                },
            )
            time.sleep(0.4)

        print("[NOTIFICATION] Sent new jobs to Discord.")
