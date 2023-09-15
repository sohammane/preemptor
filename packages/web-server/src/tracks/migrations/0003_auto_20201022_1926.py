# Generated by Django 3.0.3 on 2020-10-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_auto_20200717_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='datetime_created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='track',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]