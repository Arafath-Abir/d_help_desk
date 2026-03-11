from django.contrib import admin
from .models import Ticket, TicketAttachment, TicketComment

# Allows adding attachments directly from the Ticket admin page
class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1

# Allows adding comments directly from the Ticket admin page
class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_id",
        "student",
        "department",
        "status",
        "assigned_to",
        "created_at",
    )
    list_filter = ("status", "department")
    search_fields = ("ticket_id", "subject")
    inlines = [TicketAttachmentInline, TicketCommentInline] # Visual ease for manager

@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "uploaded_at")

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author", "is_internal", "created_at")
    list_filter = ("is_internal",)