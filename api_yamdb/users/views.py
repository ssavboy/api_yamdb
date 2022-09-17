from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


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


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
