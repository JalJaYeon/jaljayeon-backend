from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.user.views import UserView
from apps.sleep.views import SleepView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, basename='users')
router.register(r'sleep', SleepView, basename='sleep')

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
]

urlpatterns += router.urls