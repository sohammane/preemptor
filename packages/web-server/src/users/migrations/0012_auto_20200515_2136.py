# Generated by Django 3.0.3 on 2020-05-15 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('users', '0011_auto_20200515_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='institutions',
            field=models.ManyToManyField(blank=True, related_name='users', to='institutions.Institution'),
        ),
    ]
