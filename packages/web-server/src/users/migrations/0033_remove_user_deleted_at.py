# Generated by Django 3.0.3 on 2021-03-11 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20210128_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deleted_at',
        ),
    ]