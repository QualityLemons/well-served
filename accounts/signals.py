from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from archive.models import AuditLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='login',
        ip_address=request.META.get('REMOTE_ADDR'),
        metadata={'user_agent': request.META.get('HTTP_USER_AGENT')}
    )