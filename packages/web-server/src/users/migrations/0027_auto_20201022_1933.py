# Generated by Django 3.0.3 on 2020-10-22 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20201016_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='datetime_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='datetime_updated',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]