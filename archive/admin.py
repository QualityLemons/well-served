from django.contrib import admin

from .models import AuditLog, ToolInstance, ToolSession, WaitingListEntry


@admin.register(ToolSession)
class ToolSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tool_slug', 'host', 'status', 'created_at', 'closed_at')
    list_filter = ('status', 'tool_slug')
    search_fields = ('tool_slug', 'host__email')
    readonly_fields = ('id', 'created_at')


@admin.register(ToolInstance)
class ToolInstanceAdmin(admin.ModelAdmin):
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


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'resource_id', 'ip_address')
    list_filter = ('action',)
    search_fields = ('user__email', 'resource_id')
    readonly_fields = ('timestamp',)
