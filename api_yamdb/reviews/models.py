from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.IntegerField('Год выпуска')
    description = models.TextField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True,
        blank=True
    )

    def __str__(self):
        return self.name

# перенести константы в settings
# MAXIMUM_SCORE = 10
# SCORE_CHOICES = range(1, MAXIMUM_SCORE)


OUTPUT_LIMIT = 60


class Review(models.Model):
    """Описание модели Review."""
    review = models.TextField(max_length=3000)
    score = models.IntegerField(
        choices=[(x, str(x)) for x in range(1, 25)],
        default='5'
    )
# написать валидатор на максимальное значение    ????
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        default='admin',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.review[:OUTPUT_LIMIT]


class Comment(models.Model):
    """Описание модели Comment."""
    comment = models.TextField(max_length=3000)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        default='admin',
    )
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.review[:OUTPUT_LIMIT]
