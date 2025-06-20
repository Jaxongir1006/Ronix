from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactUs

@receiver(post_save, sender=ContactUs)
def send_contact_message_to_admin(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f"Yangi murojaat: {instance.name}",
            message=f"Ism: {instance.name}\nEmail: {instance.email}\n\nXabar:\n{instance.message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
        )