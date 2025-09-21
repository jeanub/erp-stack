from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer, UserTokenObtainPairSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    """Issue JWT pairs with user metadata embedded in the response."""

    permission_classes = [AllowAny]
    serializer_class = UserTokenObtainPairSerializer


class CurrentUserView(APIView):
    """Return the authenticated user's information."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("roles").order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdmin]
