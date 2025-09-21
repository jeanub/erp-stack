from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    EMPLOYEE = "employee"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"
    ROLE_CHOICES = [(EMPLOYEE,"Empleado"),(SUPERVISOR,"Supervisor"),(ADMIN,"Administrador")]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)

    @property
    def is_manager(self):  # supervisor o admin
        return self.role in {self.SUPERVISOR, self.ADMIN}
