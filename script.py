import google.generativeai as genai
from dotenv import load_dotenv
from instagrapi import Client
import random
import time
import os

load_dotenv()

ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

business_info = """
We are a custom cake shop based in Chennai.
- Prices start from ₹500
- Delivery available within 15km
- Custom designs possible
"""

def generate_reply(chat_history):
    prompt = f"""You are a helpful assistant for a custom cake shop. Always respond professionally and clearly.

Business Info:
{business_info}

Chat History:
{chat_history}

Reply:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini API error:", e)
        return None

cl = Client()
try:
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
    unreads = cl.direct_threads(selected_filter="unread")

    for thread in unreads:
        chat_history = ""

        for message in reversed(thread.messages):
            role = "system" if message.user_id == curr_user_id else "user"
            chat_history += f"{role}: {message.text}\n"

        print("⬇️ Chat history:\n", chat_history)

        reply = generate_reply(chat_history)
        reply = reply.strip()
        if reply:
            print("🤖 Replying with:\n", reply)
            cl.direct_send(
                text=reply, 
                thread_ids=[thread.id]
            )

        sleep_duration_for_a_thread = random.uniform(10, 20)
        print("⏸️ Sleeping between threads for:", sleep_duration_for_a_thread)
        time.sleep(sleep_duration_for_a_thread)

    sleep_duration_for_all_threads = random.uniform(60, 120)
    print("⏸️ Sleeping between polling rounds:", sleep_duration_for_all_threads)
    time.sleep(sleep_duration_for_all_threads)
