from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from api_yamdb import settings


from users.models import User
from .validators import validate_year


class CategoryGenre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField('Название', max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(
        'Описание', max_length=200, null=True, blank=True
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles', null=True, blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name

class TextBase(models.Model):
    """Абстрактная модель для Review и Comment."""

class Review(models.Model):
    """Описание модели Review."""

    text = models.TextField(max_length=3000)
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)s_related',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract=True
        ordering = ('pub_date',)
    
    def __str__(self):
        return self.text[:settings.OUTPUT_LIMIT]


    
class Review(TextBase):
    """Описание модели Review."""

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10)
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta(TextBase.Meta):
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_for_a_title'
            )
        ]


class Comment(TextBase):
    """Описание модели Comment."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рецензия'
    )

    class Meta(TextBase.Meta):
        verbose_name='Комментарий'
        verbose_name_plural='Комментарии'
