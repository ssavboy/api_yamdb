from django.db import models


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
