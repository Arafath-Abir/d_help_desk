from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import User, StudentProfile
from .serializers import (
    LoginSerializer,
    UserSerializer,
    StudentProfileSerializer,
    AgentListSerializer,
    StudentListSerializer,
)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data

        profile_data = None
        if request.user.role == "STUDENT":
            try:
                profile = request.user.student_profile
                profile_data = StudentProfileSerializer(profile).data
            except StudentProfile.DoesNotExist:
                profile_data = None

        return Response(
            {
                "user": user_data,
                "student_profile": profile_data
            },
            status=status.HTTP_200_OK
        )


class AgentListView(generics.ListAPIView):
    serializer_class = AgentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role="AGENT", is_active=True).order_by("full_name")


class StudentListView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role="STUDENT", is_active=True).order_by("full_name")