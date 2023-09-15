# Generated by Django 3.0.3 on 2020-09-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='has_face',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='has_screen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='has_typing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='has_voice',
            field=models.BooleanField(default=False),
        ),
    ]
