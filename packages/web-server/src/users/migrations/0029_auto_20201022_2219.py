# Generated by Django 3.0.3 on 2020-10-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20201022_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(3, 'Student'), (2, 'Professor'), (1, 'Admin'), (4, 'Supervisor')], default=3, null=True),
        ),
    ]
