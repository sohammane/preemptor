# Generated by Django 3.0.3 on 2020-06-04 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20200521_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_tdna_text',
            field=models.TextField(blank=True),
        ),
    ]
