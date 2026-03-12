from rest_framework import generics
from .models import Ticket, TicketComment, TicketActivityLog, TicketAttachment
from .permissions import IsStudent, IsManager, IsAgent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .serializers import (
    TicketSerializer,
    TicketCreateSerializer,
    TicketAssignSerializer,
    AgentTicketUpdateSerializer,
    TicketCommentSerializer,
    TicketActivityLogSerializer,
    TicketAttachmentSerializer,


)


class StudentTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Ticket.objects.filter(student=self.request.user).order_by("-created_at")


class StudentTicketCreateView(generics.CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        ticket = serializer.save()

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=self.request.user,
            action="TICKET_CREATED",
            description=f"Ticket {ticket.ticket_id} was created by student."
        )



class ManagerTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        queryset = Ticket.objects.all().order_by("-created_at")

        status = self.request.query_params.get("status")
        department = self.request.query_params.get("department")
        ticket_id = self.request.query_params.get("ticket_id")

        if status:
            queryset = queryset.filter(status=status)

        if department:
            queryset = queryset.filter(department_id=department)

        if ticket_id:
            queryset = queryset.filter(ticket_id__icontains=ticket_id)

        return queryset


class ManagerTicketAssignView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketAssignSerializer
    permission_classes = [IsManager]
    lookup_field = "id"

    def perform_update(self, serializer):
        ticket = serializer.save()

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=self.request.user,
            action="TICKET_ASSIGNED",
            description=f"Ticket assigned to {ticket.assigned_to.full_name if ticket.assigned_to else 'No Agent'} with status {ticket.status}."
        )


class AgentAssignedTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAgent]

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user).order_by("-created_at")


class AgentTicketUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AgentTicketUpdateSerializer
    permission_classes = [IsAgent]
    lookup_field = "id"

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        ticket = serializer.save()

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=self.request.user,
            action="STATUS_UPDATED",
            description=f"Agent updated ticket status to {ticket.status}."
        )

class StudentTicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsStudent]
    lookup_field = "id"

    def get_queryset(self):
        return Ticket.objects.filter(student=self.request.user)


class ManagerTicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsManager]
    lookup_field = "id"

    def get_queryset(self):
        return Ticket.objects.all()


class AgentTicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAgent]
    lookup_field = "id"

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)


class TicketCommentListView(generics.ListAPIView):
    serializer_class = TicketCommentSerializer

    def get_queryset(self):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        if user.role == "MANAGER":
            return TicketComment.objects.filter(ticket_id=ticket_id).order_by("created_at")

        if user.role == "AGENT":
            return TicketComment.objects.filter(
                ticket_id=ticket_id,
                ticket__assigned_to=user
            ).order_by("created_at")

        if user.role == "STUDENT":
            return TicketComment.objects.filter(
                ticket_id=ticket_id,
                ticket__student=user,
                is_internal=False
            ).order_by("created_at")

        return TicketComment.objects.none()

def perform_create(self, serializer):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        try:
            if user.role == "MANAGER":
                ticket = Ticket.objects.get(id=ticket_id)

            elif user.role == "AGENT":
                ticket = Ticket.objects.get(id=ticket_id, assigned_to=user)

            elif user.role == "STUDENT":
                ticket = Ticket.objects.get(id=ticket_id, student=user)
            else:
                raise Ticket.DoesNotExist

        except Ticket.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to comment on this ticket.")

        comment = serializer.save(ticket=ticket, author=user)

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=user,
            action="COMMENT_ADDED",
            description=f"New comment added to ticket. Internal: {comment.is_internal}"
        )


class TicketActivityLogListView(generics.ListAPIView):
    serializer_class = TicketActivityLogSerializer

    def get_queryset(self):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        if user.role == "MANAGER":
            return TicketActivityLog.objects.filter(ticket_id=ticket_id).order_by("-created_at")

        if user.role == "AGENT":
            return TicketActivityLog.objects.filter(
                ticket_id=ticket_id,
                ticket__assigned_to=user
            ).order_by("-created_at")

        if user.role == "STUDENT":
            return TicketActivityLog.objects.filter(
                ticket_id=ticket_id,
                ticket__student=user
            ).order_by("-created_at")

        return TicketActivityLog.objects.none()

class TicketCommentCreateView(generics.CreateAPIView):
    serializer_class = TicketCommentSerializer

    def perform_create(self, serializer):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        try:
            if user.role == "MANAGER":
                ticket = Ticket.objects.get(id=ticket_id)

            elif user.role == "AGENT":
                ticket = Ticket.objects.get(id=ticket_id, assigned_to=user)

            elif user.role == "STUDENT":
                ticket = Ticket.objects.get(id=ticket_id, student=user)
            else:
                raise Ticket.DoesNotExist

        except Ticket.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to comment on this ticket.")

        comment = serializer.save(ticket=ticket, author=user)

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=user,
            action="COMMENT_ADDED",
            description=f"New comment added to ticket. Internal: {comment.is_internal}"
        )

class TicketAttachmentListView(generics.ListAPIView):
    serializer_class = TicketAttachmentSerializer

    def get_queryset(self):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        if user.role == "MANAGER":
            return TicketAttachment.objects.filter(ticket_id=ticket_id).order_by("-uploaded_at")

        if user.role == "AGENT":
            return TicketAttachment.objects.filter(
                ticket_id=ticket_id,
                ticket__assigned_to=user
            ).order_by("-uploaded_at")

        if user.role == "STUDENT":
            return TicketAttachment.objects.filter(
                ticket_id=ticket_id,
                ticket__student=user
            ).order_by("-uploaded_at")

        return TicketAttachment.objects.none()


class TicketAttachmentCreateView(generics.CreateAPIView):
    serializer_class = TicketAttachmentSerializer

    def perform_create(self, serializer):
        ticket_id = self.kwargs["id"]
        user = self.request.user

        try:
            if user.role == "MANAGER":
                ticket = Ticket.objects.get(id=ticket_id)

            elif user.role == "AGENT":
                ticket = Ticket.objects.get(id=ticket_id, assigned_to=user)

            elif user.role == "STUDENT":
                ticket = Ticket.objects.get(id=ticket_id, student=user)

            else:
                raise Ticket.DoesNotExist

        except Ticket.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to upload attachment on this ticket.")

        attachment = serializer.save(ticket=ticket)

        TicketActivityLog.objects.create(
            ticket=ticket,
            user=user,
            action="ATTACHMENT_ADDED",
            description=f"Attachment added: {attachment.file.name}"
        )


class ManagerDuplicateTicketView(APIView):
    permission_classes = [IsManager]

    def post(self, request, id):
        try:
            original_ticket = Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        new_ticket = Ticket.objects.create(
            student=original_ticket.student,
            department=original_ticket.department,
            subject=original_ticket.subject,
            description=original_ticket.description,
            status=Ticket.Status.OPEN
        )

        TicketActivityLog.objects.create(
            ticket=new_ticket,
            user=request.user,
            action="TICKET_DUPLICATED",
            description=f"Ticket duplicated from {original_ticket.ticket_id}"
        )

        TicketActivityLog.objects.create(
            ticket=original_ticket,
            user=request.user,
            action="TICKET_DUPLICATED",
            description=f"Ticket duplicated to {new_ticket.ticket_id}"
        )

        return Response(
            {"message": "Ticket duplicated successfully"},
            status=status.HTTP_201_CREATED
        )


class ManagerDashboardStatsView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        data = {
            "total_tickets": Ticket.objects.count(),
            "open_tickets": Ticket.objects.filter(status="OPEN").count(),
            "assigned_tickets": Ticket.objects.filter(status="ASSIGNED").count(),
            "in_progress_tickets": Ticket.objects.filter(status="IN_PROGRESS").count(),
            "resolved_tickets": Ticket.objects.filter(status="RESOLVED").count(),
            "closed_tickets": Ticket.objects.filter(status="CLOSED").count(),
        }

        return Response(data)