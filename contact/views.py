from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .forms import contactForm


# Create your views here.

def contact(request):
    title = 'Contact'
    form = contactForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        message = '%s %s' % (comment, name)
        emailFrom = form.cleaned_data['email']
        print(emailFrom)
        emailTo = [settings.EMAIL_HOST_USER,]
        subject = 'BomBox: %s' % (emailFrom)
        send_mail(subject, message, emailFrom, emailTo, fail_silently=False)
        title = 'Thanks'
        confirm_message = 'Thanks for your input. We will get right back to you '
        form = None

    context = {'title': title, 'form': form, 'confirm_message': confirm_message, }
    template = 'contact.html'
    return render(request, template, context)
