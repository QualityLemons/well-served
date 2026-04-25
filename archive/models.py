import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class ToolSession(models.Model):
    """A collaborative session of a tool, hosted by one user.

    Other logged-in users join via the session's URL. Each participant's
    contribution is captured as its own ``ToolInstance`` linked back to the
    session. Closing the session locks every contribution and triggers the
    tool's processing logic so a combined view can be shown.
    """

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_sessions',
    )
    tool_slug = models.CharField(max_length=100)
    tool_version = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    timer_started_at = models.DateTimeField(
        null=True, blank=True,
        help_text='Set when the host starts the phase timer so all clients stay in sync.',
    )
    timer_paused_at = models.DateTimeField(
        null=True, blank=True,
        help_text='Set when the host pauses the timer; cleared on resume or reset.',
    )
    timer_elapsed_before_pause = models.FloatField(
        default=0,
        help_text='Cumulative elapsed seconds before the current (or last) pause.',
    )

    md_file = models.FileField(upload_to='archives/md/', null=True, blank=True)
    rtf_file = models.FileField(upload_to='archives/rtf/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tool_slug} session ({self.status}) hosted by {self.host}'


class ToolInstance(models.Model):
    """A user-scoped record of a tool draft / submission."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tool_instances',
    )

    session = models.ForeignKey(
        ToolSession,
        on_delete=models.CASCADE,
        related_name='instances',
        null=True,
        blank=True,
        help_text='Set when this instance is part of a collaborative session.',
    )

    tool_slug = models.CharField(max_length=100)
    tool_version = models.CharField(max_length=20)

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    payload_input = models.JSONField(default=dict, help_text='The raw user inputs.')
    payload_output = models.JSONField(
        default=dict, null=True, blank=True, help_text="The tool's result."
    )

    html_file = models.FileField(upload_to='archives/html/', null=True, blank=True)
    md_file = models.FileField(upload_to='archives/md/', null=True, blank=True)
    rtf_file = models.FileField(upload_to='archives/rtf/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'],
                name='unique_session_user_instance',
                condition=models.Q(session__isnull=False),
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.tool_slug} ({self.status})'

    def archive_record(self):
        if self.status == 'draft':
            self.status = 'archived'
            self.submitted_at = now()
            self.save()


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('submit', 'Tool Submission'),
        ('download', 'File Download'),
        ('access_denied', 'Unauthorized Access Attempt'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.action} @ {self.timestamp:%Y-%m-%d %H:%M}'
