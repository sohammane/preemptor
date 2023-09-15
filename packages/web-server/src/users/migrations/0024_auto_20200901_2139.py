# Generated by Django 3.0.3 on 2020-09-01 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20200817_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='academic_level',
            field=models.TextField(choices=[('H', 'High School'), ('C', 'College'), ('M', 'Master'), ('D', 'Doctor'), ('O', 'Other')], default='H', max_length=1),
        ),
    ]