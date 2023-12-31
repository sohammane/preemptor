# Generated by Django 3.0.3 on 2020-08-13 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20200807_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.TextField(choices=[('D', 'Draft'), ('O', 'Open'), ('I', 'In Progress'), ('R', 'In Revision'), ('G', 'Graded')], default='D', max_length=1),
        ),
    ]
