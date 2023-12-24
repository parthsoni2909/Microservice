from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','token','first_name', 'last_name', 'email', 'phone_number', 'password')
    
    def get_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0]
        return token.key


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginGetOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


class ChangePasswordsSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "old_password", "new_password"]


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = User.objects.filter(email=email)

            if user:
                if not user[0].is_active:
                    msg = _("User account is disabled.")
                    raise exceptions.ValidationError(msg)
            else:
                msg = _("User account not found")
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data["user"] = user[0]
        return data
