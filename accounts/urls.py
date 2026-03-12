from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    MeView,
    AgentListView,
    StudentListView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("agents/", AgentListView.as_view(), name="agent-list"),
    path("students/", StudentListView.as_view(), name="student-list"),
]