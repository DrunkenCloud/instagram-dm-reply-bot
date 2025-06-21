import os
import re
import csv
import time
import random
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

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

def load_contacts(csv_path):
    contacts = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append(row)
    return contacts

def load_templates(folder_path):
    templates = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                templates.append(f.read())
    return templates

def personalize(template, contact):
    def replacer(match):
        key = match.group(1).strip()
        return contact.get(key, f"{{{{{key}}}}}")
    return re.sub(r'{{(.*?)}}', replacer, template)

def send_message(contact, templates):
    username_guess = contact.get("username")
    if not username_guess:
        print(f"❌ No username for contact: {contact}")
        return

    users = cl.search_users(username_guess)
    if not users:
        print(f"❌ No user found for guessed username: {username_guess}")
        return

    user_id = users[0].pk
    selected_template = random.choice(templates)
    message = personalize(selected_template, contact)

    try:
        cl.direct_send(message, user_ids=[user_id])
        print(f"✅ Sent to {username_guess} (actual: {users[0].username})")
    except Exception as e:
        print(f"❌ Failed to send to {username_guess}: {e}")

if __name__ == "__main__":
    contacts = load_contacts("contacts.csv")
    templates = load_templates("templates")

    for contact in contacts:
        send_message(contact, templates)

        sleep_duration_for_a_thread = random.uniform(20, 40)
        print("⏸️ Sleeping between COntacts for:", sleep_duration_for_a_thread)
        time.sleep(sleep_duration_for_a_thread)
