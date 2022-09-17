from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = (
    (USER, 'User'),
    (ADMIN, 'Moderator'),
    (MODERATOR, 'Admin'))


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True)
    email = models.EmailField(
        max_length=254,
        unique=True)
    first_name = models.CharField(
        verbose_name='Имя пользователя.',
        max_length=150,
        blank=True,
        null=True)
    last_name = models.CharField(
        verbose_name='Фамилия пользователя.',
        max_length=150,
        blank=True,
        null=True)
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
        blank=True)
    confirm_code = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
