import os
import email
import re
from dotenv import load_dotenv
from imapclient import IMAPClient
from bs4 import BeautifulSoup  # New import for parsing HTML

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT"))

EMAIL_FETCH_LIMIT = 5  # Limit the number of unread emails

def extract_text_from_email(parsed_email):
    """
    Extracts plain text from an email, handling HTML emails properly.
    """
    body = ""

    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":  # Prefer plain text if available
                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                break
            elif content_type == "text/html":  # If only HTML is available, extract text
                html_content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html_content, "html.parser")
                body = soup.get_text()  # Extract visible text from HTML
                break
    else:
        body = parsed_email.get_payload(decode=True).decode("utf-8", errors="ignore")

    # Remove excessive whitespace and line breaks
    body = re.sub(r"\n\s*\n", "\n", body).strip()
    return body

def fetch_unread_emails():
    """
    Fetches unread emails and returns them as a list of dictionaries.
    """
    emails = []
    with IMAPClient(IMAP_SERVER, port=IMAP_PORT, ssl=True) as client:
        try:
            client.login(EMAIL, PASSWORD)
            client.select_folder("INBOX", readonly=True)

            messages = client.search(["UNSEEN"])
            if not messages:
                print("📭 No unread emails.")
                return []

            print(f"📬 Found {len(messages)} unread emails. Processing the first {EMAIL_FETCH_LIMIT}:")
            messages = messages[:EMAIL_FETCH_LIMIT]  # Limit results

            for msg_id in messages:
                raw_message = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
                parsed_email = email.message_from_bytes(raw_message)

                subject = parsed_email["subject"]
                sender = parsed_email["from"]
                body = extract_text_from_email(parsed_email)  # Use the improved extraction function

                emails.append({"from": sender, "subject": subject, "body": body})

        except Exception as e:
            print("⚠️ Error fetching emails:", e)

    return emails  # Return the list of email data

if __name__ == "__main__":
    fetched_emails = fetch_unread_emails()
    print(f"\n📥 Processed {len(fetched_emails)} unread emails.")
