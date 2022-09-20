from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.TextField('Название', max_length=200)
    year = models.IntegerField('Год выпуска')
    rating = models.IntegerField('Рейтинг', null=True, default=None)
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

class TextBase(models.Model):
    """Абстрактная модель для Review и Comment."""

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

