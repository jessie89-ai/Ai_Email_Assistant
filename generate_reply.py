import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

MAX_INPUT_LENGTH = 500  # Limit email body length

def generate_ai_reply(email_subject, email_body):
    """
    Uses OpenAI to generate a reply based on the email subject and body.
    """
    try:
        # Truncate long emails to prevent API errors
        if len(email_body) > MAX_INPUT_LENGTH:
            email_body = email_body[:MAX_INPUT_LENGTH] + "..."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": 
                    "You are a professional AI email assistant. "
                    "Your responses should be polite, well-structured, and human-like. "
                    "Ensure the response is helpful and formal but friendly."},
                {"role": "user", "content": 
                    f"Email Subject: {email_subject}\n"
                    f"Email Body: {email_body}\n"
                    "Generate a well-structured, professional, and natural email reply."}
            ]
        )

        ai_reply = response.choices[0].message.content.strip()
        return ai_reply

    except Exception as e:
        print("⚠️ Error:", e)
        return "Sorry, I couldn't generate a response."

# Test the function
if __name__ == "__main__":
    test_subject = "Meeting Request"
    test_body = "Hi, can we schedule a meeting for next week to discuss our project?"
    
    reply = generate_ai_reply(test_subject, test_body)
    print("\n🤖 AI Generated Reply:\n", reply)

    