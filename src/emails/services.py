from .models import Email, EmailVerificationEvent
from django.core.mail import send_mail
from django.conf import settings

def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    verification_obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email
    )
    did_send = send_verification_email(verification_obj)
    return verification_obj, did_send

def send_verification_email(verification_obj):
    text_msg: str|None = get_verification_email_msg(verification_obj, as_html=False)
    text_html = get_verification_email_msg(verification_obj, as_html=True)

    subject = "Please Verify Your Email - From Django"
    from_email = settings.EMAIL_HOST_USER
    to_email = verification_obj.email

    return send_mail(
        subject,
        text_msg,
        from_email,
        [to_email],
        fail_silently=False,
        html_message=text_html
    )


def get_verification_email_msg(verification_instance, as_html=False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return ""
    if as_html:
        return f"<h1>{verification_instance.pk}</h1>"
    return f"{verification_instance.pk}"