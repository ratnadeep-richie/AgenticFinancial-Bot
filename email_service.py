import smtplib
from email.mime.text import MIMEText


def send_email_alert(to_email, subject, message):

    # 🔴 REPLACE THESE WITH YOUR EMAIL + APP PASSWORD
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    if not to_email:
        return  # Avoid crash if email missing

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print("Email failed:", e)
