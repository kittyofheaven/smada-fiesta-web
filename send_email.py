import os
from re import template
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from jinja2 import Environment, FileSystemLoader
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

from dotenv import load_dotenv
load_dotenv('.env')

import smtplib
from email.message import EmailMessage
class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


# conf = ConnectionConfig(
#     MAIL_USERNAME=Envs.MAIL_USERNAME,
#     MAIL_PASSWORD=Envs.MAIL_PASSWORD,
#     MAIL_FROM=Envs.MAIL_FROM,
#     MAIL_PORT=Envs.MAIL_PORT,
#     MAIL_SERVER=Envs.MAIL_SERVER,
#     MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     TEMPLATE_FOLDER='./templates/email'
# )



# async def send_email_async(subject: str, email_to: str, body: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body,
#         subtype='html',
#     )

#     fm = FastMail(conf)

#     await fm.send_message(message, template_name='email.html')


# def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: list, body: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body,
#         subtype='html',
#     )

#     fm = FastMail(conf)

#     background_tasks.add_task(
#         fm.send_message, message, template_name='email.html')


def send_email(reciever, subject, body) :

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Envs.MAIL_FROM
    msg['To'] = reciever
    # msg.set_content(body)

    template = env.get_template('email.html')
    output = template.render(title = 'Confirmation', name = 'John Doe') 
    # with open('templates\email.html', 'r') as f:
        # msg.set_content(f.read())
    msg.add_alternative(output, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Envs.MAIL_USERNAME, Envs.MAIL_PASSWORD)
        smtp.send_message(msg)

def send_email_background(background_tasks: BackgroundTasks, subject: str, reciever: str, body: str):
    background_tasks.add_task(send_email, reciever, subject, body)