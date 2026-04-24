def log_action(user, action, resource_id=None, metadata=None):
    from .models import AuditLog
    AuditLog.objects.create(
        user=user,
        action=action,
        resource_id=str(resource_id) if resource_id else None,
        metadata=metadata or {}
    )