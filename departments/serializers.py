from rest_framework import serializers
from .models import Department, AgentDepartment


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "is_active",
        ]


class AgentDepartmentSerializer(serializers.ModelSerializer):
    agent_id = serializers.IntegerField(source="agent.id", read_only=True)
    agent_name = serializers.CharField(source="agent.full_name", read_only=True)
    agent_email = serializers.CharField(source="agent.email", read_only=True)
    department_id = serializers.IntegerField(source="department.id", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = AgentDepartment
        fields = [
            "id",
            "agent_id",
            "agent_name",
            "agent_email",
            "department_id",
            "department_name",
            "assigned_at",
        ]