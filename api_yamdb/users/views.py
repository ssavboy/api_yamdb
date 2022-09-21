from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

from api.permissions import IsAdmin
from .models import User
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data)


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        try:
            user, is_created = User.objects.get_or_create(
                email=email,
                username=username)
        except IntegrityError:
            raise ValidationError(
                detail={username: 'Этот username уже занят.',
                        email: 'Этот email уже занят.'})
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код под подтверждения: ',
            message=f'Код подтверждения - "{confirmation_code}".',
            from_email=None,
            recipient_list=(email,))
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': ['Invalid token!']},
            status=status.HTTP_400_BAD_REQUEST)
