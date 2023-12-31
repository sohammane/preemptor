# Generated by Django 3.0.3 on 2020-10-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20201016_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(3, 'Student'), (2, 'Professor'), (1, 'Admin')], default=3, null=True),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
