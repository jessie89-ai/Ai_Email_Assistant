import os
import json
import logging
from generate_reply import generate_ai_reply
from read_email import fetch_unread_emails

# Set up logging
logging.basicConfig(filename="email_bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# File to store replies
REPLY_FILE = "replies.json"

def load_existing_replies():
    """
    Loads existing replies, ensuring the file is a valid JSON format.
    If the file is missing or corrupted, it resets it.
    """
    try:
        if not os.path.exists(REPLY_FILE):
            return []  # If the file doesn't exist, return an empty list

        with open(REPLY_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()  # Read and remove extra spaces
            if not content:
                return []  # If the file is empty, return an empty list
            return json.loads(content)  # Load JSON data

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"❌ Error loading replies.json: {e}. Resetting file.")
        return []  # If file is corrupt, return an empty list

def save_reply(email_sender, email_subject, ai_reply):
    """
    Stores AI-generated replies in a JSON file for review.
    """
    try:
        if not ai_reply.strip():
            logging.error(f"❌ OpenAI returned an empty response for {email_subject}. Skipping storage.")
            print(f"⚠️ Skipping empty AI reply for: {email_subject}")
            return  # Skip saving this email reply

        reply_data = {
            "sender": email_sender,
            "subject": email_subject,
            "reply": ai_reply
        }

        # Load existing replies safely
        existing_replies = load_existing_replies()

        # Add new reply
        existing_replies.append(reply_data)

        # Save back to file
        with open(REPLY_FILE, "w", encoding="utf-8") as file:
            json.dump(existing_replies, file, indent=4)

        print(f"✅ Reply stored for review: {email_sender} | {email_subject}")
        logging.info(f"Reply stored for {email_sender} | Subject: {email_subject}")

    except Exception as e:
        print("⚠️ Error storing reply:", e)
        logging.error(f"Error storing reply: {e}")

def process():
    """
    Process unread emails and generate replies.
    """
    try:
        print("🔍 Fetching unread emails...")
        unread_emails = fetch_unread_emails()

        if not unread_emails:
            print("📭 No unread emails found.")
            logging.info("📭 No unread emails found.")
            return

        print(f"📬 Processing {len(unread_emails)} unread emails...")
        for email in unread_emails:
            email_sender = email['from']
            email_subject = email['subject']
            email_body = email['body']
            
            print(f"📩 Generating AI reply for: {email_subject} from {email_sender}")
            ai_reply = generate_ai_reply(email_subject, email_body)

            print(f"🤖 AI Generated Reply: {ai_reply[:100]}...")  # Print first 100 characters
            save_reply(email_sender, email_subject, ai_reply)

        print("✅ Finished processing all unread emails.")

    except Exception as e:
        print("⚠️ Error processing emails:", e)
        logging.error(f"Error processing emails: {e}")

if __name__ == "__main__":
    process()
