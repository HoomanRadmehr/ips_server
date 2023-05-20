from django.core.mail import EmailMessage,get_connection
from ips_server.settings import EMAIL_HOST,EMAIL_PORT,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
import smtplib
import logging
import traceback


def send_email(data):
    try:
        email = EmailMessage(subject=data['subject'],body=data['body'],to=[data['to'],])
        email.send(fail_silently=False)
    except:
        logging.error(traceback.format_exc())
    