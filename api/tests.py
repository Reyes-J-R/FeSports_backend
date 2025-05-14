from django.test import TestCase
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "futureesportsgaming@gmail.com"
receiver_email = "reyesjoeroshan@gmail.com"
password = "qlwp bale jikm eolo"
smtp_server = "smtp.gmail.com"
smtp_port = 587

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email"

body = "<h1>TEST EMAIL</h1>"
message.attach(MIMEText(body, "html"))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)

"""ball_triangle
bars
circles
grid
hearts
oval
puff
rings
spinning_circles
tail_spin
three_dots"""