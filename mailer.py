import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mail_self(address, password, subject, body = ""):
    msg = MIMEMultipart("alternative")
    msg["From"] = address
    msg["To"] = address
    msg["Subject"] = subject
    body = MIMEText(body)
    msg.attach(body)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(address, password)
    s.sendmail(address, address, msg.as_string())
    s.quit()