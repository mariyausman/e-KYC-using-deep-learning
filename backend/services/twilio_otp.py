from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
client = Client(account_sid, auth_token)

def send_otp(phone_number):
    verification = client.verify.v2.services(verify_service_sid).verifications.create(
        to=phone_number,
        channel='sms'
    )
    return verification.status == 'pending'

def verify_otp(phone_number, otp_code):
    verification_check = client.verify.v2.services(verify_service_sid).verification_checks.create(
        to=phone_number,
        code=otp_code
    )
    return verification_check.status == "approved"
