import streamlit as st
import json
import os
from send_email import send_email
from read_email import fetch_unread_emails  # Import function to fetch emails

# File to store replies
REPLY_FILE = "replies.json"

# 🔒 Simple authentication
def check_password():
    """Returns `True` if the user enters the correct password and clicks login."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    password = st.text_input("Enter Password:", type="password")

    if st.button("Login"):  
        correct_password = os.getenv("DASHBOARD_PASSWORD", "your_secure_password")  # Default if env var missing

        if password == correct_password:
            st.session_state["authenticated"] = True
        elif password.lower() == "guest":
            st.session_state["authenticated"] = "guest"
        else:
            st.error("Incorrect password. Try again.")

    return st.session_state["authenticated"]

if not check_password():
    st.stop()  # Stop app if not logged in

# 🔄 Load stored AI replies
def load_replies():
    """Loads stored AI replies from replies.json."""
    try:
        with open(REPLY_FILE, "r", encoding="utf-8") as file:
            replies = json.load(file)
        return replies
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# 🗑️ Delete a reply
def delete_reply(index):
    """Deletes a reply from the list."""
    replies = load_replies()
    if index < len(replies):
        del replies[index]
        with open(REPLY_FILE, "w", encoding="utf-8") as file:
            json.dump(replies, file, indent=4)
        st.success("Reply deleted successfully!")

# 🔄 Refresh Emails
def refresh_emails():
    """Fetch new unread emails after deleting."""
    st.session_state["emails"] = fetch_unread_emails()

# 📩 AI Job Inquiry Sender
def generate_job_email():
    """AI-generated job inquiry email sender."""
    job_description = st.text_area("Describe the Job You Want (e.g., 'Software Engineer role')", "")
    
    if st.button("Generate & Send AI Job Inquiry"):
        if job_description.strip():
            ai_reply = f"Dear Hiring Manager,\n\nI am very interested in the {job_description} position. I would love to discuss how my skills can contribute to your company.\n\nBest regards,\n[Your Name]"
            send_email("your-email@gmail.com", f"Job Inquiry: {job_description}", ai_reply)
            st.success("✅ AI-generated job inquiry email sent to your inbox!")
        else:
            st.error("❌ Please describe the job before sending.")

# 🌟 Main Dashboard UI
def main():
    st.title("📧 AI Email Assistant Dashboard")
    st.write("Review, edit, and send AI-generated replies.")

    # 🔄 Refresh Emails Button
    if st.button("🔄 Refresh Emails"):
        refresh_emails()

    # 📩 Handle Guest Mode
    if st.session_state["authenticated"] == "guest":
        st.info("👤 Guest mode active. Displaying sample emails.")
        replies = [
            {"sender": "recruiter@company.com", "subject": "Exciting Job Opportunity!", "reply": "Hi, I'm interested!"},
            {"sender": "hr@techcorp.com", "subject": "Software Engineer Interview", "reply": "Looking forward to it!"},
        ]
    else:
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

    # 📩 Add AI Job Inquiry Feature Below Replies
    st.subheader("📨 AI Job Inquiry Generator")
    generate_job_email()

if __name__ == "__main__":
    main()
