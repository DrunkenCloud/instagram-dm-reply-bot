from dotenv import load_dotenv
from instagrapi import Client
import random
import time
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

cl = None

try:
    cl = Client()
    
    if os.path.exists("session.json"):
        print("📂 Loading existing session...")
        cl.load_settings("session.json")
        print("✅ Session loaded successfully!")
    else:
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        cl.dump_settings("session.json")
        
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit(1)

curr_user_id = cl.user_id

while True:
    # unreads = cl.direct_threads(selected_filter="unread")
    unreads = cl.direct_threads()

    for thread in unreads:
        chat_history = ""

        for message in thread.messages:
            if message.user_id == curr_user_id:
                chat_history += "system: "
            else:
                chat_history += "user: "
            chat_history += message.text + "\n"
        
        print(chat_history)

        sleep_duration_for_a_thread = random.uniform(10, 20)
        print("Sleeping between threads for: ", sleep_duration_for_a_thread)
        time.sleep(sleep_duration_for_a_thread)

    sleep_duration_for_all_threads = random.uniform(60, 120)
    print("Sleeping between all threads polling: ", sleep_duration_for_all_threads)
    time.sleep(sleep_duration_for_all_threads)