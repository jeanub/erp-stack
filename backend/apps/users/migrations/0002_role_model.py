# Generated manually to introduce Role model and migrate existing user roles.
from django.db import migrations, models


ROLE_DEFINITIONS = (
    ("admin", "Administrador"),
    ("supervisor", "Supervisor"),
    ("employee", "Empleado"),
)


def create_roles(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    for code, name in ROLE_DEFINITIONS:
        Role.objects.get_or_create(code=code, defaults={"name": name})


def migrate_user_roles(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    User = apps.get_model("users", "User")

    roles_by_code = {role.code: role for role in Role.objects.all()}

    for user in User.objects.all():
        legacy = getattr(user, "role", None)
        if legacy:
            role_obj = roles_by_code.get(legacy)
            if role_obj:
                user.roles.add(role_obj)

        if not user.roles.exists():
            default_code = "admin" if getattr(user, "is_superuser", False) else "employee"
            role_obj = roles_by_code.get(default_code)
            if role_obj:
                user.roles.add(role_obj)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=64, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.CharField(blank=True, max_length=255)),
            ],
            options={"ordering": ["code"]},
        ),
        migrations.AddField(
            model_name="user",
            name="roles",
            field=models.ManyToManyField(blank=True, related_name="users", to="users.role"),
        ),
        migrations.RunPython(create_roles, migrations.RunPython.noop),
        migrations.RunPython(migrate_user_roles, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
    ]
