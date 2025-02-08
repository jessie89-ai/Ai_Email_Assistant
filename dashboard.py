import streamlit as st
import json
from send_email import send_email

# File to store replies
REPLY_FILE = "replies.json"

def load_replies():
    """Loads stored AI replies from replies.json."""
    try:
        with open(REPLY_FILE, "r", encoding="utf-8") as file:
            replies = json.load(file)
        return replies
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def delete_reply(index):
    """Deletes a reply from the list."""
    replies = load_replies()
    if index < len(replies):
        del replies[index]
        with open(REPLY_FILE, "w", encoding="utf-8") as file:
            json.dump(replies, file, indent=4)
        st.success("Reply deleted successfully!")

def main():
    st.title("📧 AI Email Assistant Dashboard")
    st.write("Review, edit, and send AI-generated replies.")

    replies = load_replies()

    if not replies:
        st.info("📭 No AI replies available. Run the email processor first.")
        return

    for index, reply in enumerate(replies):
        with st.expander(f"📩 {reply['subject']} - {reply['sender']}"):
            st.write("### AI-Generated Reply")
            edited_reply = st.text_area("Edit Reply", value=reply["reply"], height=150)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"✅ Send Reply to {reply['sender']}", key=f"send_{index}"):
                    send_email(reply["sender"], "Re: " + reply["subject"], edited_reply)
                    delete_reply(index)  # Remove from stored replies after sending
                    st.experimental_rerun()

            with col2:
                if st.button("🗑️ Delete Reply", key=f"delete_{index}"):
                    delete_reply(index)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
