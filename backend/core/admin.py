from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Member, Invoice

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'license_number', 'phone')
    search_fields = ('first_name', 'last_name', 'email', 'license_number')
    list_filter = ('created_at',)

@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'member', 'amount', 'status', 'date_issued')
    list_filter = ('status', 'date_issued')
    search_fields = ('member__first_name', 'member__last_name', 'description')
