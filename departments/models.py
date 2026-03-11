from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True) # e.g., CSE, ADMIN
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AgentDepartment(models.Model):
    # Links an Agent to a specific department
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agent_departments",
        limit_choices_to={"role": "AGENT"},
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_agents",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("agent", "department")

    def __str__(self):
        return f"{self.agent.username} -> {self.department.name}"