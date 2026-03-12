from rest_framework import serializers
from .models import Ticket, TicketComment, TicketActivityLog, TicketAttachment
from departments.models import AgentDepartment


class TicketSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.full_name", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_id",
            "student",
            "student_name",
            "department",
            "department_name",
            "subject",
            "description",
            "status",
            "assigned_to",
            "assigned_to_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["ticket_id", "created_at", "updated_at"]


class TicketCreateSerializer(serializers.ModelSerializer):
    def validate_subject(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Subject must be at least 5 characters.")
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        return Ticket.objects.create(
            student=request.user,
            **validated_data
        )

    class Meta:
        model = Ticket
        fields = ["department", "subject", "description"]


class TicketAssignSerializer(serializers.ModelSerializer):

    def validate_assigned_to(self, value):
        if value.role != "AGENT":
            raise serializers.ValidationError("Only agents can be assigned to tickets.")

        ticket = self.instance

        is_valid_agent = AgentDepartment.objects.filter(
            agent=value,
            department=ticket.department
        ).exists()

        if not is_valid_agent:
            raise serializers.ValidationError("This agent is not assigned to the ticket department.")

        return value

    def update(self, instance, validated_data):
        agent = validated_data.get("assigned_to")

        if agent:
            instance.assigned_to = agent
            instance.status = Ticket.Status.ASSIGNED

        instance.save()
        return instance

    class Meta:
        model = Ticket
        fields = ["assigned_to"]


class AgentTicketUpdateSerializer(serializers.ModelSerializer):
    def validate_status(self, value):
        allowed_statuses = ["IN_PROGRESS", "RESOLVED", "CLOSED"]

        if value not in allowed_statuses:
            raise serializers.ValidationError("Agent can only set status to IN_PROGRESS, RESOLVED, or CLOSED.")

        return value

    class Meta:
        model = Ticket
        fields = ["status"]


class TicketCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)

    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.user.role == "STUDENT" and attrs.get("is_internal"):
            raise serializers.ValidationError("Students cannot create internal comments.")

        return attrs

    class Meta:
        model = TicketComment
        fields = [
            "id",
            "ticket",
            "author",
            "author_name",
            "comment",
            "is_internal",
            "created_at",
        ]
        read_only_fields = ["ticket", "author", "created_at"]


class TicketActivityLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = TicketActivityLog
        fields = [
            "id",
            "ticket",
            "user",
            "user_name",
            "action",
            "description",
            "created_at",
        ]


class TicketAttachmentSerializer(serializers.ModelSerializer):
    def validate_file(self, value):
        allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
        max_size = 5 * 1024 * 1024

        file_name = value.name.lower()

        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError("Only JPG, JPEG, PNG, and PDF files are allowed.")

        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 5 MB.")

        return value

    class Meta:
        model = TicketAttachment
        fields = [
            "id",
            "ticket",
            "file",
            "uploaded_at",
        ]
        read_only_fields = ["ticket", "uploaded_at"]