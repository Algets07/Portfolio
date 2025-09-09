from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Project
from .forms import ContactForm

def home(request):
    projects = Project.objects.all()
    form = ContactForm()
    success_message = None  # for showing feedback

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # Save to DB

            # Email to you (site owner)
            send_mail(
                subject=f"New Contact from {contact.name}",
                message=f"""
You have a new contact submission:

Name: {contact.name}
Email: {contact.email}

Message:
{contact.message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['algetss223@gmail.com'],  # your receiving email
                fail_silently=False,
            )

            # Optional: Auto-reply to sender
            send_mail(
    subject="Thank you for contacting us",
    message=f"""
Hello {contact.name},

Thank you for reaching out to us. We have received your message and We will get back to you shortly.  

Best regards,  
Algets S  
""",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[contact.email],  # Send to the user who filled the form
    fail_silently=False,
)

            success_message = "✅ Your message has been sent successfully!"
            form = ContactForm()  # Clear form
            

    return render(request, 'home.html', {
        'projects': projects,
        'form': form,
        'success_message': success_message
    })
