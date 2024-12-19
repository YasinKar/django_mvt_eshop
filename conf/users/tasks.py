from celery import shared_task
import time

@shared_task(queue='tasks')
def send_sms_task(phone, otp_code):
    time.sleep(5) # simulation of a long task
    return f'sms sent to {phone} and otp was : {otp_code}'
