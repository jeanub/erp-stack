from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """System role that can be assigned to users."""

    EMPLOYEE = "employee"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover - human readable helper
        return self.name or self.code


class User(AbstractUser):
    EMPLOYEE = Role.EMPLOYEE
    SUPERVISOR = Role.SUPERVISOR
    ADMIN = Role.ADMIN

    roles = models.ManyToManyField(Role, related_name="users", blank=True)

    def has_role(self, role_code: str) -> bool:
        if not role_code:
            return False
        return self.roles.filter(code=role_code).exists()

    @property
    def primary_role(self) -> str | None:
        return self.roles.order_by("code").values_list("code", flat=True).first()

    @property
    def role(self) -> str | None:  # backwards compatibility accessor
        return self.primary_role

    @property
    def is_manager(self) -> bool:  # supervisor o admin
        return self.has_role(self.SUPERVISOR) or self.has_role(self.ADMIN)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.roles.exists():
            default_code = self.ADMIN if self.is_superuser else self.EMPLOYEE
            default_role = Role.objects.filter(code=default_code).first()
            if default_role:
                self.roles.add(default_role)
