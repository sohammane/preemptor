# Generated by Django 3.0.3 on 2020-04-29 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('users', '0007_auto_20200429_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='institutions',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='institutions.Institution'),
        ),
    ]
