from .models import Email, EmailVerificationEvent

def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email
    )
    return obj

def get_verification_email_msg(verification_instance, as_html=False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    if as_html:
        return f"<h1>{verification_instance.pk}</h1>"
    return f"{verification_instance.pk}"