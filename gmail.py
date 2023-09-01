import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os



load_dotenv()

def send_email(email, body, name):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender = os.getenv('SENDER_EMAIL')  # Enter your address
    receiver = os.getenv('RECEIVER_EMAIL')  # Enter receiver address
    password = os.getenv('APP_PW')

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f"Message from {name}, Email: {email}"
    msg['From'] = sender
    msg['To'] = receiver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.send_message(msg, from_addr=sender, to_addrs=receiver)
