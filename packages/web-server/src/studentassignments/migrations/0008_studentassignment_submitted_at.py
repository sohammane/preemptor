# Generated by Django 3.0.3 on 2021-02-23 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentassignments', '0007_auto_20210223_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentassignment',
            name='submitted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
