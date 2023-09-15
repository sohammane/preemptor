# Generated by Django 3.0.3 on 2020-08-13 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20200807_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_face',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='has_typing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='has_voice',
            field=models.BooleanField(default=False),
        ),
    ]
