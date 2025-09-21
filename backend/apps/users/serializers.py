from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role, User


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field="code",
        queryset=Role.objects.all(),
        required=False,
    )
    role = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    role_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "roles",
            "role_names",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["date_joined", "role_names"]

    def create(self, validated_data):
        roles = self._extract_roles(validated_data)
        user = super().create(validated_data)
        self._sync_roles(user, roles)
        return user

    def update(self, instance, validated_data):
        roles = self._extract_roles(validated_data)
        user = super().update(instance, validated_data)
        self._sync_roles(user, roles)
        return user

    def _extract_roles(self, validated_data):
        roles = validated_data.pop("roles", None)
        single_role = validated_data.pop("role", None)

        role_objects = list(roles) if roles is not None else None

        if single_role:
            try:
                role_obj = Role.objects.get(code=single_role)
            except Role.DoesNotExist as exc:
                raise serializers.ValidationError({"role": "Invalid role code."}) from exc

            if role_objects is None:
                role_objects = [role_obj]
            elif all(existing.pk != role_obj.pk for existing in role_objects):
                role_objects.append(role_obj)

        return role_objects

    def _sync_roles(self, user: User, roles):
        if roles is None:
            return
        user.roles.set(roles)

    def get_role_names(self, user: User) -> list[dict[str, str]]:
        return [
            {"code": role.code, "name": role.name}
            for role in user.roles.all().order_by("code")
        ]


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize token payload to include user metadata."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["roles"] = list(user.roles.values_list("code", flat=True))
        token["role"] = user.primary_role
        token["username"] = user.username
        if user.email:
            token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        data["role"] = self.user.primary_role
        data["roles"] = list(self.user.roles.values_list("code", flat=True))
        return data
