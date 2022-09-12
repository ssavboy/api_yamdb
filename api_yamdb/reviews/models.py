from django.db import models

# перенести константы в settings
MAXIMUM_SCORE = 10
SCORE_CHOICES = range(1, MAXIMUM_SCORE)

class Review(models.Model):
    """Описание модели Review."""

    review = models.TextField(max_length=3000)
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
# написать валидатор на максимальное значение    ???? 
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True
    )


class Comment(models.Model):
    """Описание модели Comment."""

    comment = models.TextField(max_length=3000)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата создания', auto_now_add=True
    )


    pass
