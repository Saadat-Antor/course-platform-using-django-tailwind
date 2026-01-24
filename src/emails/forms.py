from django import forms
from . import css
from .models import Email, EmailVerificationEvent

class EmailForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-input",
                "class": css.EMAIL_INPUT_CSS,
                "placeholder": "youremail@example.com"
            }
        )
    )

    class Meta:
        model = EmailVerificationEvent
        fields = ['email']