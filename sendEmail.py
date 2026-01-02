### ---- To send email 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
senderEmail = "madhurask375@gmail.com"
receiverEmail = "madhura@techpunditsinc.com"
password = "pikg hgye ngoc cpyf"
subject = "Test"
body = "Hello, this is a test email"
msg = MIMEMultipart()
msg["From"] = senderEmail
msg["To"] = receiverEmail
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(senderEmail, password)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print("Error:", e)