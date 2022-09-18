from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategoriesSerializer, CommentSerializer
from .serializers import GenreSerializer, TitleSerializer
from .serializers import ReviewSerializer, ReadOnlyTitleSerializer
from reviews.models import Category, Genre, Title, Review
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для запросов к объектам Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(ListCreateDestroyViewSet):
    """Вьюсет для запросов к объектам Category."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов к объектам Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов к объектам Review."""

    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Выбор разрешений исходя из типа запроса"""
        if self.action == 'destroy' or self.action == 'update':
            return (IsAuthorModeratorAdminOrReadOnly(),)
        return super().get_permissions()

    def get_title(self):
        """Определение объекта Title, связанного с Review."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Определение множества объектов Review."""
        return self.get_title().reviews.select_related('title')

    def perform_create(self, serializer):
        """Переопределение метода создания объекта Review."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов к объектам Comment."""

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Выбор разрешений исходя из типа запроса"""
        if self.action == 'destroy' or self.action == 'update':
            return (IsAuthorModeratorAdminOrReadOnly(),)
        return super().get_permissions()

    def get_review(self):
        """Определение объекта Review, связанного с Comment."""

        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Определение множества объектов Comment."""
        return self.get_review().comments.select_related('review')

    def perform_create(self, serializer):
        """Переопределение метода создания объекта Comment."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
