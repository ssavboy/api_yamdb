# Generated by Django 2.2.16 on 2022-09-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(blank=True, max_length=70, null=True, unique=True),
        ),
    ]
