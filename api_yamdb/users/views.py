from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer

codegen = default_token_generator


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = UserSerializer
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, is_created = User.objects.get_or_create(
            email=email,
            username=username
        )
        confirm_token = codegen.make_token(user)
        mail_subject = 'Your verification token'
        message = f'Confirmation token - {confirm_token}'

        send_mail(
            mail_subject,
            message,
            'example@mail.com',
            (email,)
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confir_token = serializer.validated_data.get('confir_token')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if codegen.check_token(user, confir_token):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confir_token': ['Invalid code!']},
            status=status.HTTP_400_BAD_REQUEST)
