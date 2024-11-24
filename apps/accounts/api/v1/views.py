from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from apps.accounts.models import Personalization
from .serializers import PersonalizationSerializer

@api_view(['GET'])
def get_routes(request):
    routes = {
        "Auth Endpoints": {
            "User Registration": "/api/v1/auth/users/",
            "User Login (JWT)": "/api/v1/auth/jwt/create/",
            "User Logout (JWT)": "/api/v1/auth/token/blacklist/",
            "Token Refresh": "/api/v1/auth/jwt/refresh/",
            "User Activation": "/api/v1/auth/users/activation/",
            "Password Reset": "/api/v1/auth/users/reset_password/",
            "Password Reset Confirm": "/api/v1/auth/users/reset_password_confirm/",
            "Resend Activation": "/api/v1/auth/users/resend_activation/",
            "Set New Password": "/api/v1/auth/users/set_password/",
            "User Profile": "/api/v1/auth/users/me/",
            "Delete User": "/api/v1/auth/users/{id}/",
            "User List (Admin)": "/api/v1/auth/users/",
            "User Detail (Admin)": "/api/v1/auth/users/{id}/",
        }
    }
    return Response(routes)

class PersonalizationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Personalization instances.
    """
    serializer_class = PersonalizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optionally, restrict to the authenticated user's personalization
        return Personalization.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)