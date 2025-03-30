from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet, UserRegisterView, home_view, DashboardStatsView, UsernameUpdateView
from .views import (
    UploadedFileViewSet,
    UserRegisterView,
    home_view,
    DashboardStatsView,
    UsernameUpdateView  # ✅ Add this import
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'files', UploadedFileViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('profile/update-username/', UsernameUpdateView.as_view(), name='update-username'),
  # ✅ Correct route
]

# 👇 Add DRF router URLs (for files)
urlpatterns += router.urls

