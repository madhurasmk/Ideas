### -------- Program that copies the link copied in LinkedIn to an Excel file  -----------
### ---- Have created a .bat file and save it in the startup dir. 
### ---- When the system starts the file executes the .bat file and waits until a link is copied from a LinkedIn post

import time
import os
import pyperclip
import pandas as pd
from datetime import datetime

EXCEL_FILE = r"C:\\CSR\\ml_vector_py\\linkedin_saved_articles.xlsx"

CHECK_INTERVAL = 1

last_seen = None

def is_linkedin_url(text):
    return isinstance(text, str) and "linkedin.com" in text and text.startswith("http")

def save_link(link):
    data = {
        "Link": [link],
        "Saved On": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        if link in df["Link"].values:
            return
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)

    df.to_excel(EXCEL_FILE, index=False)
    print("✔ Saved:", link)

print(" Clipboard watcher running... Copy a LinkedIn link")

while True:
    try:
        current = pyperclip.paste()

        if current != last_seen:
            last_seen = current
            if is_linkedin_url(current):
                save_link(current)

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")
        break


### ---- Stub to check if clipboard copy works -------
# import pyperclip
# import time

# print("Copy ANY text now...")
# time.sleep(3)

# print("Clipboard contains:")
# print(pyperclip.paste())
