# Generated by Django 3.0.3 on 2021-01-15 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='score',
            new_name='quality',
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.TextField(choices=[(1, 'Typing Verification Failure')], max_length=1),
        ),
    ]
