from rest_framework import serializers

from .models import User
from .mixins import UsernameValidatorMixin
from api_yamdb import settings


class UserSerializer(serializers.ModelSerializer, UsernameValidatorMixin):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class SignUpSerializer(serializers.Serializer, UsernameValidatorMixin):
    username = serializers.CharField(max_length=settings.RESTRICT_NAME)
    email = serializers.EmailField(max_length=settings.RESTRICT_EMAIL)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer, UsernameValidatorMixin):
    username = serializers.CharField(
        required=True, max_length=settings.RESTRICT_NAME)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
