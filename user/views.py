from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, VerifyAccountSerializer, LoginSerializer, LoginGetOtpSerializer, UserAccountUpdateSerializer, ChangePasswordsSerializer,PasswordResetRequestSerializer, PasswordResetSerializer
from django.core.mail import send_mail
from django.conf import settings
import random
from rest_framework.response import Response
from twilio.rest import Client 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegistrationViewSet(ModelViewSet):
    """
        register - API for User Registration.

        # Sample Request Data
            {
                "first_name": "Parth",
                "last_name": "Soni",
                "email": "soniparth2909@gmail.com",
                "phone_number": 919427654588,
                "password": "Secure@098"
            }
        # Success Response Data
            {
                "success": true,
                "message": "User register successfully. PLease check you email for the account verification."
            }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    
    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        email = serializer.validated_data["email"]
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]
        
        if User.objects.filter(email=email).exists():
            return Response(
            {
                "success": False,
                "message": "User is already exists with this Email ID.",
            },
            status=status.HTTP_200_OK,
        )

        user = User.objects.create(first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            username="{}{}".format(first_name.lower(), last_name.lower()))
        user.set_password(password)
        user.save()

        if User.objects.filter(email=email).exists():
            otp = random.randint(100000, 999999)
        User.objects.filter(email=email).update(otp=otp)

        subject = "Account Verification Email"
        message = f"You account is verification otp is {otp}"
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True)


        return Response(
            {
                "success": True,
                "message": "User register successfully. PLease check you email for the account verification.",
            },
            status=status.HTTP_200_OK,
        )


class VerifyAccountViewSet(ModelViewSet):
    """
        AccountVetification - API for User Account verify.

        # Sample Request Data
            {
                "email": "soniparth2909@gmail.com",
                "otp": "921359"
            }

        # Success Response Data
            {
                "success": true,
                "message": "Your account verified successfully"
            }
        
        # Invadil OTP Response Data
            {
                "success": false,
                "message": "Invalid OTP"
            }
        
        # Invadil Eamil Response Data
            {
                "success": false,
                "message": "Invalid Email Address"
            }
    """
    serializer_class = VerifyAccountSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        otp = serializer.data["otp"]

        user = User.objects.filter(email=email).first()
        if user:
            if user.otp != otp:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid OTP",
                    },
                    status=status.HTTP_200_OK,
                )

            user.is_verified = True
            user.save()

            return Response(
                {
                    "success": True,
                    "message": "Your account verified successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Email Address",
                },
                status=status.HTTP_200_OK,
            )
        

class LoginGetOtpViewSet(ModelViewSet):
    """
        LogInOTP - API for get otp via SMS for login.

        # Sample Request Data
            {
                "phone_number": "919427654588"
            }

        # Success Response Data
            {
                "success": true,
                "message": "OTP sent successfully"
            }
        
        # User not found with thw phone number Response Data
            {
                "success": false,
                "message": "User not found with this phone number"
            }
    """
    serializer_class = LoginGetOtpSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        if User.objects.filter(phone_number=phone_number).exists():
            login_otp = str(random.randint(100000, 999999))
            User.objects.filter(phone_number=phone_number).update(login_otp=login_otp)

            # Twilio integration
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            from_phone_number = settings.TWILIO_PHONE_NUMBER
            to_phone_number = f'+{phone_number}'

            client = Client(account_sid, auth_token)

            message_body = f'Your OTP is: {login_otp}'

            message = client.messages.create(
                body=message_body,
                from_=from_phone_number,
                to=to_phone_number
            )

            return Response(
                {'success':True,'message': 'OTP sent successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success':False,'message': 'User not found with this phone number'},
                status=status.HTTP_404_NOT_FOUND
            )

    
class LoginViewSet(ModelViewSet):
    """
        LogIn - API for login.

        # Sample Request Data
            {
                "phone_number": "919427654588",
                "otp": "661163"
            }

        # Success Response Data
            {
                "success": true,
                "message": "Loggedin successfully",
                "payload": {
                    "id": 2,
                    "token": "3383e07d5af243fc9de2c966cff129959f7e410b",
                    "first_name": "Parth",
                    "last_name": "Soni",
                    "email": "soniparth2909@gmail.com",
                    "phone_number": 919427654588,
                    "password": "pbkdf2_sha256$320000$MtHS1aaIdwNwiW2847J5A6$c/9U6LYZdzFS6Wi5OKZ4NQ2pDsqCFc/NhIcwB78fAy8="
                }
            }
        
        # Invadil OTP Response Data
            {
                "success": false,
                "message": "Invalid OTP"
            }
        
        # Invadil Eamil Response Data
            {
                "success": false,
                "message": "Invalid Phone number"
            }
    """
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            if user.login_otp != otp:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid OTP"
                    },
                    status=status.HTTP_200_OK,
                )

            serializer = UserSerializer(user)
            return Response(
                {
                    "success": True,
                    "message": "Loggedin successfully",
                    'payload': serializer.data
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Phone number",
                },
                status=status.HTTP_200_OK,
            )
        

class GetUserViewset(ModelViewSet):
    """
        GetUser - API for get user data.

        # Success Response Data
            {
                "success": true,
                "message": "Get User Data Successfully",
                "payload": {
                    "id": 2,
                    "token": "3383e07d5af243fc9de2c966cff129959f7e410b",
                    "first_name": "Parth",
                    "last_name": "Soni",
                    "email": "soniparth2909@gmail.com",
                    "phone_number": 919427654588,
                    "password": "pbkdf2_sha256$320000$MtHS1aaIdwNwiW2847J5A6$c/9U6LYZdzFS6Wi5OKZ4NQ2pDsqCFc/NhIcwB78fAy8="
                }
            }
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    http_method_names = ["get"]
    queryset = User.objects.all()

    def list(self, request):
        user_id = self.request.user.id
        user_data = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(user_data)

        return Response(
            {
                "success": True,
                "message": "Get User Data Successfully",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

class UserAccountUpdateViewSet(ModelViewSet):
    """
        UpdateUserAccount/{user_id} - API for update user data.

        # Sample Request Data
            {
                "first_name": "Parth S",
                "last_name": "Soni",
                "phone_number": 916355361115
            }

        # Success Response Data
            {
                "success": true,
                "message": "Account information updated successfully",
                "payload": {
                    "first_name": "Parth S",
                    "last_name": "Soni",
                    "phone_number": 916355361115
                }
            }
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountUpdateSerializer
    http_method_names = ["put"]
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "success": True,
                "message": "Account information updated successfully",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

class ChangePasswordViewSet(ModelViewSet):
    """
        ChangePassword/{user_id} - API for change password.

        # Sample Request Data
            {
                "old_password": "Secure@098",
                "new_password": "Parth@2909"
            }

        # Success Response Data
            {
                "success": true,
                "message": "Your Password Changed Successfully."
            }
        
        # Old Password wrong Response Data
            {
                "success": false,
                "meaasage": "Old password id wrong"
            }

        # New Password is same as old password Response Data
            {
                "success": false,
                "message": "New password cannot be the same as the old password."
            }
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordsSerializer
    http_method_names = ["put"]
    queryset = User.objects.all()

    def update(self, request, pk=None):
        serializer = ChangePasswordsSerializer(data=request.data)
        user = User.objects.get(pk=request.user.id)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response(
                    {"success": False, "meaasage": "Old password id wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user.check_password(new_password):
                return Response(
                    {
                        "success": False,
                        "message": "New password cannot be the same as the old password.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"success": True, "message": "Your Password Changed Successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestViewSet(ModelViewSet):
    """
        ResetPasswordEmail - API for request reset password.

        # Sample Request Data
            {
                "email": "soniparth2909@gmail.com"
            }

        # Success Response Data
            {
                "success": true,
                "message": "Password reset link sent to your email address. Please check your email."
            }
        
        # Email wrong Response Data
            {
                "success": false,
                "message": "User not found with the provided email address."
            }
    """
    serializer_class = PasswordResetRequestSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            current_site = request.build_absolute_uri("/")
            reset_link = f"{current_site}api/v1/users/ResetPassword/" # update you reset password page url.
            subject = "Password Reset Link"
            message = f"Click the following link to reset your password: {reset_link}"
            recipient_list = [email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True)

            return Response(
                {
                    "success": True,
                    "message": "Password reset link sent to your email address. Please check your email.",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "User not found with the provided email address.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class PasswordResetViewSet(ModelViewSet):
    """
        ResetPassword - API for reset password.

        # Sample Request Data
            {
                "email": "soniparth2909@gmail.com",
                "password": "Secure@098"
            }

        # Success Response Data
            {
                "success": true,
                "message": "User Password Updated"
            }
    """
    serializer_class = PasswordResetSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]

        if User.objects.filter(email=email).exists():
            user = serializer.validated_data["user"]
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                {"success": True, "message": "User Password Updated"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "message": "User not exist with this emai address"},
            status=status.HTTP_201_CREATED,
        )