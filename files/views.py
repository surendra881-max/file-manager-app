from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.http import JsonResponse, FileResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from collections import Counter
from django.db import models

from .models import UploadedFile
from .serializers import (
    UploadedFileSerializer,
    UserRegisterSerializer,
    UsernameUpdateSerializer
)

# 🌐 Home View
def home_view(request):
    return JsonResponse({"message": "Welcome to the File Manager API!"})

# 📁 Uploaded File ViewSet
class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 🆕 Download file by ID
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        try:
            uploaded_file = self.get_object()
            return FileResponse(uploaded_file.file.open(), as_attachment=True, filename=uploaded_file.file.name)
        except Exception as e:
            raise Http404("File not found.")

# 👤 User Registration View
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["username", "email", "password"]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"error": f"{field.capitalize()} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if User.objects.filter(username=data["username"]).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=data["username"],
            email=data["email"],
            password=make_password(data["password"])
        )
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

# 📊 Dashboard Statistics View
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        files = UploadedFile.objects.all()
        total_files = files.count()

        # Breakdown by file extension
        file_types = [f.file.name.split('.')[-1].lower() for f in files]
        type_counts = dict(Counter(file_types))

        # Upload count by user
        user_uploads = (
            files.values('user__username')
            .annotate(count=models.Count('id'))
            .order_by('-count')
        )
        uploads_by_user = {entry['user__username']: entry['count'] for entry in user_uploads}

        return Response({
            "total_files": total_files,
            "file_types": type_counts,
            "files_by_user": uploads_by_user
        })

# 🛠️ Username Update View
class UsernameUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = UsernameUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Username updated successfully!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .models import UserProfile, Address
from .serializers import UserProfileSerializer, PhoneUpdateSerializer, AddressSerializer, AddressCreateUpdateSerializer

# 📱 View or Edit Phone Number (Full Profile)
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

# 📞 Update Only Phone Number
class PhoneUpdateView(generics.UpdateAPIView):
    serializer_class = PhoneUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

# 🏠 View All Addresses of User
class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile.addresses.all()

# ➕ Add New Address
class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(user_profile=profile)

# ✏️ Update / 🗑️ Delete Address
class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile.addresses.all()
