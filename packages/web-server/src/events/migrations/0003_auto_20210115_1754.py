# Generated by Django 3.0.3 on 2021-01-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20210115_1734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['status', '-id']},
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.TextField(choices=[('P', 'Pending'), ('A', 'In Analysis'), ('X', 'Closed')], default='P', max_length=1),
        ),
    ]
