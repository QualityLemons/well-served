from django.contrib import admin

from .models import AuditLog, FeatureRequest, ToolInstance, ToolSession, WaitingListEntry


@admin.register(ToolSession)
class ToolSessionAdmin(admin.ModelAdmin):
    """Admin view for collaborative ToolSession records."""

    list_display = ('id', 'tool_slug', 'host', 'status', 'created_at', 'closed_at')
    list_filter = ('status', 'tool_slug')
    search_fields = ('tool_slug', 'host__email')
    readonly_fields = ('id', 'created_at')


@admin.register(ToolInstance)
class ToolInstanceAdmin(admin.ModelAdmin):
    """Admin view for individual ToolInstance draft and archived records."""

    list_display = ('id', 'user', 'tool_slug', 'tool_version', 'status',
                    'session', 'created_at', 'submitted_at')
    list_filter = ('status', 'tool_slug')
    search_fields = ('tool_slug', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WaitingListEntry)
class WaitingListEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'signed_up_at')
    search_fields = ('email', 'name')
    readonly_fields = ('signed_up_at',)


@admin.register(FeatureRequest)
class FeatureRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'email', 'submitted_at')
    search_fields = ('title', 'description', 'name', 'email')
    readonly_fields = ('submitted_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Read-oriented admin view for the AuditLog security table.

    No custom delete action is registered here; the standard Django admin
    delete action remains available, which is intentional — administrators
    may need to purge logs for legal or data-retention reasons.  The
    ``timestamp`` field is read-only to prevent tampering via the admin UI.
    """

    list_display = ('timestamp', 'user', 'action', 'resource_id', 'ip_address')
    list_filter = ('action',)
    search_fields = ('user__email', 'resource_id')
    readonly_fields = ('timestamp',)
