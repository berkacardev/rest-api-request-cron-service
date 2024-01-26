import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
sender_mail = os.getenv("SENDER_MAIL")
sender_mail_app_key = os.getenv("SENDER_MAIL_APP_KEY")
target_mails = os.getenv("TARGET_MAIL").split(',')
request_url = os.getenv("REQUEST_URL")
token = os.getenv("TOKEN")
user_token_id = os.getenv("USER_TOKEN_ID")
user_authorization = os.getenv("USER_AUTHORIZATION")


def send_mail(response_status_code):
    subject = ""
    content = ""
    if response_status_code == 200:
        subject = "(Sucsess) Sucsess Message"
        content = "Sucess " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif response_status_code == 500:
        subject = "(Error) Error Message"
        content = "Error 500 " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = MIMEText(content)
    message['From'] = sender_mail
    message['To'] = ", ".join(target_mails)
    message['Subject'] = subject
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender_mail, sender_mail_app_key)
        mail.sendmail(sender_mail, target_mails, message.as_string())
        mail.close()
    except Exception as e:
        print(e)


def do_request():
    request_header = {'token': token, "userTokenId": user_token_id, "Authorization": user_authorization}
    response = requests.post(request_url, headers=request_header)
    return response.status_code


def start_process():
    response_code = do_request()
    if response_code == 500:
        for i in range(3):
            if do_request() == 200:
                break
            if do_request() == 500 and i == 2:
                send_mail(500)
    elif response_code == 200:
        send_mail(200)


start_process()
