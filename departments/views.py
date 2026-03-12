from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Department, AgentDepartment
from .serializers import DepartmentSerializer, AgentDepartmentSerializer


class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Department.objects.filter(is_active=True).order_by("name")


class DepartmentAgentListView(generics.ListAPIView):
    serializer_class = AgentDepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        department_id = self.kwargs["id"]
        return AgentDepartment.objects.filter(
            department_id=department_id,
            agent__is_active=True
        ).select_related("agent", "department").order_by("agent__full_name")