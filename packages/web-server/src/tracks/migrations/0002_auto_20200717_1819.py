# Generated by Django 3.0.3 on 2020-07-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='metadata',
            field=models.TextField(blank=True, null=True),
        ),
    ]
