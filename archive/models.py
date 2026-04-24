class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('submit', 'Tool Submission'),
        ('download', 'File Download'),
        ('access_denied', 'Unauthorized Access Attempt'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_id = models.CharField(max_length=100, null=True, blank=True) # e.g., ToolInstance ID
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict) # To store browser info or specific tool slugs

    class Meta:
        ordering = ['-timestamp']