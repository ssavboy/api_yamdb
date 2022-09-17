from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_username(self, data):
        if data.lower() == 'me':
            raise ValidationError(message='username cannot equal "me".')
        return data
    
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirm_code = serializers.CharField()
