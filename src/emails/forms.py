from django import forms
from . import css, services
from .models import Email, EmailVerificationEvent

class EmailForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-input",
                "class": css.EMAIL_INPUT_CSS,
                "placeholder": "youremail@example.com"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        verified = services.verify_email(email)
        if verified:
            raise forms.ValidationError(f"Invalid email `{email}`! Please try again.")
        return email

    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']