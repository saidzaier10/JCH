from django.contrib import admin
from .models import EmailTemplate, EmailLog

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('key', 'subject', 'updated_at')
    search_fields = ('key', 'subject')

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('recipient', 'subject')
    readonly_fields = ('recipient', 'subject', 'status', 'error_message', 'created_at')
