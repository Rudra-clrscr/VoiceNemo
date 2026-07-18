import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_reminder(to_email: str, subject: str, body: str) -> str:
    """Sends a reminder email via Gmail SMTP using an App Password."""
    try:
        smtp_email = os.getenv("SMTP_EMAIL")
        smtp_password = os.getenv("SMTP_APP_PASSWORD")

        if not smtp_email or not smtp_password:
            return (
                "Email not configured. Please add SMTP_EMAIL and SMTP_APP_PASSWORD "
                "to your .env file. You can generate an App Password at "
                "https://myaccount.google.com/apppasswords"
            )

        # Build the email
        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Plain text version
        msg.attach(MIMEText(body, "plain"))

        # HTML version with NovaVoice branding
        html_body = f"""
        <html>
        <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                      background: #121212; color: #ffffff; padding: 2rem;">
            <div style="max-width: 500px; margin: 0 auto; background: #1e1e1e; 
                        border-radius: 8px; padding: 2rem; border: 2px solid #000000; box-shadow: 4px 4px 0px #000000;">
                <h2 style="color: #ff5722; margin-top: 0; font-weight: 700; letter-spacing: -0.01em;">🔔 VoiceNemo Reminder</h2>
                <p style="font-size: 1.05rem; line-height: 1.6; color: #e0e0e0;">{body}</p>
                <hr style="border: none; border-top: 2px solid #000000; margin: 1.5rem 0;">
                <p style="font-size: 0.8rem; color: #a0a0a0; font-family: monospace;">
                    Sent automatically by VoiceNemo AI Assistant
                </p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, to_email, msg.as_string())

        print(f"EMAIL SENT to {to_email}: {subject}")
        return f"Success! Reminder email sent to {to_email} with subject '{subject}'."

    except smtplib.SMTPAuthenticationError:
        print("EMAIL AUTH ERROR: Invalid SMTP credentials")
        return (
            "Email authentication failed. Please check your SMTP_EMAIL and "
            "SMTP_APP_PASSWORD in the .env file. Make sure you're using a "
            "Gmail App Password, not your regular password."
        )
    except Exception as e:
        print(f"EMAIL ERROR: {e}")
        return f"Failed to send email: {str(e)}"
