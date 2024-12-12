from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models import UserProfile
from user.serializers import UserSerializer, UserLoginSerializer

# Swagger API documentation


# User registration view
class UserRegisterView(APIView):
    @swagger_auto_schema(
        operation_summary="Register a New User",
        request_body=UserSerializer,
        responses={
            201: "Register successful!",
            400: openapi.Response(
                "Validation error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error_message": openapi.Schema(type=openapi.TYPE_STRING),
                        "errors": openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["password"] = make_password(
                serializer.validated_data["password"]
            )
            serializer.save()
            return JsonResponse(
                {"message": "Register successful!"}, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            {
                "error_message": "Invalid data submitted!",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# User login view
class UserLoginView(APIView):
    @swagger_auto_schema(
        operation_summary="User Login",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                "Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING),
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                        "access_expires": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "refresh_expires": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            ),
            400: "Validation error",
            401: "Unauthorized (Invalid credentials)",
        },
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                    "access_expires": int(
                        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                    ),
                    "refresh_expires": int(
                        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                    ),
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"error_message": "Email or password is incorrect!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {"error_messages": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Get user details view
class UserGetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get User Details",
        responses={
            200: openapi.Response(
                "User details",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        # Thêm các trường khác nếu cần
                    },
                ),
            ),
            404: "User not found",
        },
    )
    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Update user details view
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update User Details",
        request_body=UserSerializer,
        responses={
            200: "User updated successfully!",
            400: "Validation error",
            404: "User not found",
        },
    )
    def put(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if "password" in serializer.validated_data:
                    serializer.validated_data["password"] = make_password(
                        serializer.validated_data["password"]
                    )
                serializer.save()
                return Response(
                    {"message": "User updated successfully!"},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Delete user view
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete User",
        responses={
            200: "User deleted successfully!",
            404: "User not found",
        },
    )
    def delete(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            user.delete()
            return Response(
                {"message": "User deleted successfully!"},
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Reset user password view
class UserResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Reset User Password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="New password"
                ),
            },
            required=["password"],
        ),
        responses={
            200: "Password reset successfully!",
            400: "Password is required",
            404: "User not found",
        },
    )
    def post(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            new_password = request.data.get("password")
            if not new_password:
                return Response(
                    {"error": "Password is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.password = make_password(new_password)
            user.save()
            return Response(
                {"message": "Password reset successfully!"},
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
