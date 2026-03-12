from django.urls import path
from .views import (
    StudentTicketListView,
    StudentTicketCreateView,
    ManagerTicketListView,
    ManagerTicketAssignView,
    AgentAssignedTicketListView,
    AgentTicketUpdateView,
    StudentTicketDetailView,
    ManagerTicketDetailView,
    AgentTicketDetailView,
    TicketCommentListView,
    TicketCommentCreateView,
    TicketActivityLogListView,
    TicketAttachmentListView,
    TicketAttachmentCreateView,
    ManagerDuplicateTicketView,
    ManagerDashboardStatsView,
)

urlpatterns = [
    path("student/tickets/", StudentTicketListView.as_view(), name="student-ticket-list"),
    path("student/tickets/create/", StudentTicketCreateView.as_view(), name="student-ticket-create"),

    path("manager/tickets/", ManagerTicketListView.as_view(), name="manager-ticket-list"),
    path("manager/tickets/<int:id>/assign/", ManagerTicketAssignView.as_view(), name="manager-ticket-assign"),

    path("agent/tickets/", AgentAssignedTicketListView.as_view(), name="agent-ticket-list"),
    path("agent/tickets/<int:id>/update/", AgentTicketUpdateView.as_view(), name="agent-ticket-update"),
    path("student/tickets/<int:id>/", StudentTicketDetailView.as_view(), name="student-ticket-detail"),
    path("manager/tickets/<int:id>/", ManagerTicketDetailView.as_view(), name="manager-ticket-detail"),
    path("agent/tickets/<int:id>/", AgentTicketDetailView.as_view(), name="agent-ticket-detail"),
    path("tickets/<int:id>/comments/", TicketCommentListView.as_view(), name="ticket-comment-list"),
    path("tickets/<int:id>/comments/create/", TicketCommentCreateView.as_view(), name="ticket-comment-create"),
    path("tickets/<int:id>/activity/", TicketActivityLogListView.as_view(), name="ticket-activity-list"),
    path("tickets/<int:id>/attachments/", TicketAttachmentListView.as_view(), name="ticket-attachment-list"),
    path("tickets/<int:id>/attachments/create/", TicketAttachmentCreateView.as_view(), name="ticket-attachment-create"),
    path("manager/tickets/<int:id>/duplicate/",ManagerDuplicateTicketView.as_view(), name="manager-ticket-duplicate",),
    path("manager/dashboard/",ManagerDashboardStatsView.as_view(), name="manager-dashboard",),
]