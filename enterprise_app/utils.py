from django.core.mail import send_mail
from django.conf import settings
from cryptography.fernet import Fernet


def send_test_email(to_email, subject, message):
    """
    Sends an email using the settings configured in settings.py

    :param to_email: Recipient email address
    :param subject: Email subject
    :param message: Email body
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # FROM email
        [to_email],                   # TO email
        fail_silently=True
    )

# Example Fernet key (you should generate your own securely)
ENCRYPTION_KEY = b'pylkmprVRkXR9HIb4Fm2mcFvxFKrC1rIKBSgWEh_FUU='
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_email(email: str) -> str:
    """Encrypt email using Fernet."""
    return fernet.encrypt(email.encode()).decode()

