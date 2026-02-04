import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('EMAIL_PASSWORD')

print('EMAIL:', repr(EMAIL))
print('PASSWORD present:', bool(PASSWORD))

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(EMAIL, PASSWORD)
        print('SMTP login: OK')
except Exception as e:
    print('SMTP login: ERROR ->', repr(e))
