# Generated by Django 3.0.3 on 2020-10-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20200515_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='datetime_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='datetime_updated',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
