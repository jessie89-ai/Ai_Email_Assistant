import json
from send_email import send_email

REPLY_FILE = "replies.json"

def send_stored_replies():
    """
    Reads stored AI replies and sends them via email.
    """
    if not REPLY_FILE or not open(REPLY_FILE).read().strip():
        print("📭 No replies to send.")
        return

    with open(REPLY_FILE, "r", encoding="utf-8") as file:
        stored_replies = json.load(file)

    for reply in stored_replies:
        sender = reply["sender"]
        subject = "Re: " + reply["subject"]
        body = reply["reply"]

        # Send the email
        send_email(sender, subject, body)

    # Clear the file after sending
    with open(REPLY_FILE, "w", encoding="utf-8") as file:
        file.write("")

    print("✅ All stored replies have been sent!")

if __name__ == "__main__":
    send_stored_replies()
