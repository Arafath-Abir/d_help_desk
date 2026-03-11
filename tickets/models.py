from django.db import models
from django.conf import settings
from departments.models import Department
import datetime

class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    ticket_id = models.CharField(max_length=30, unique=True, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submitted_tickets",
        limit_choices_to={"role": "STUDENT"},
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    
    # Internal tracking
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_tickets",
        limit_choices_to={"role": "AGENT"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate custom Ticket ID if not exists
        if not self.ticket_id:
            last_ticket = Ticket.objects.all().order_name('id').last()
            new_id = (last_ticket.id + 1) if last_ticket else 1
            self.ticket_id = f"TKT-{datetime.date.today().strftime('%Y%m')}-{new_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="ticket_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    is_internal = models.BooleanField(default=False) # Managers can use this for internal notes
    created_at = models.DateTimeField(auto_now_add=True)