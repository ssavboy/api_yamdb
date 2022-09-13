from rest_framework import viewsets
from api_yamdb.reviews.models import Review

from .serializers import CategoriesSerializer, GenreSerializer, ReviewSerializer, TitleSerializer
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Title
from reviews.models import Comment, Review


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer