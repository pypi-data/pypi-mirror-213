from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from getajob.config.settings import SETTINGS
from getajob.exceptions import EmailFailedToSendException


def send_email(to_address: str, subject: str, html_content: str):
    message = Mail(
        from_email=SETTINGS.SENDGRID_FROM_EMAIL,
        to_emails=to_address,
        subject=subject,
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(SETTINGS.SENDGRID_API_KEY)
        return sg.send(message)
    except Exception as e:
        print(e)
        raise EmailFailedToSendException
