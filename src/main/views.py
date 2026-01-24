from django.shortcuts import render
from emails.forms import EmailForm
from typing import Dict, Any
from django.conf import settings
from emails.models import Email

def home(request, *args, **kwargs):
    template_name = 'home.html'
    form = EmailForm(request.POST or None)
    context: Dict[str, Any] = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        email_value = form.cleaned_data.get('email')
        form.save()
        email_obj, created = Email.objects.get_or_create(email=email_value)
        context['form'] = EmailForm()
        context['message'] = f"Success! A verification email has been sent to you from {settings.EMAIL_ADDRESS}. Please verify. Thank you"
    return render(request, template_name, context)