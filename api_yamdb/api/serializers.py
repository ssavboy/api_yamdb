from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)


class CategoriesSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Title."""

    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Описание сериализатора для 'list' и 'retrieve'"""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Можно написать только одну рецензию на произведение.',
            )
        ]

    def validate_score(self, value):
        if value > 10:
            raise serializers.ValidationError(
                'Оценка произведения должна быть в пределах 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Описание сериализатора для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
