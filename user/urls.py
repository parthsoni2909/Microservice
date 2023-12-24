from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, VerifyAccountViewSet, LoginGetOtpViewSet,LoginViewSet,GetUserViewset, UserAccountUpdateViewSet,ChangePasswordViewSet,PasswordResetRequestViewSet, PasswordResetViewSet


router = DefaultRouter()
router.register("users/register", UserRegistrationViewSet, basename="user-registration")
router.register("users/AccountVetification", VerifyAccountViewSet, basename="user-account-verification")
router.register("users/LogInOTP", LoginGetOtpViewSet, basename="user-login-otp")
router.register("users/LogIn", LoginViewSet, basename="user-login")
router.register("users/GetUser", GetUserViewset, basename="user-data")
router.register("users/UpdateUserAccount", UserAccountUpdateViewSet, basename="user-data-update")
router.register("users/ChangePassword", ChangePasswordViewSet, basename="user-change-password")
router.register("users/ResetPasswordEmail", PasswordResetRequestViewSet, basename="user-reset-password-Email")
router.register("users/ResetPassword", PasswordResetViewSet, basename="user-reset-password")

urlpatterns = [
    path("", include(router.urls)),
]
