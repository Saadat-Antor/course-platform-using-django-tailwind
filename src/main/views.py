from django.shortcuts import render
from emails.forms import EmailForm
from typing import Dict, Any
from django.conf import settings

def home(request, *args, **kwargs):
    template_name = 'home.html'
    form = EmailForm(request.POST or None)
    context: Dict[str, Any] = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        form.save()
        context['form'] = EmailForm()
        context['message'] = f"Success! A verification email has been sent to you from {settings.EMAIL_ADDRESS}. Please verify. Thank you"
    return render(request, template_name)