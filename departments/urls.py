from django.urls import path
from .views import DepartmentListView, DepartmentAgentListView

urlpatterns = [
    path("", DepartmentListView.as_view(), name="department-list"),
    path("<int:id>/agents/", DepartmentAgentListView.as_view(), name="department-agent-list"),
]